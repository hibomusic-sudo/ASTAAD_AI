"""Facebook Messenger channel implementation."""

import asyncio
import json
from typing import Any

import aiohttp
from aiohttp import web
from loguru import logger

from deeptutor.tutorbot.bus.events import OutboundMessage
from deeptutor.tutorbot.bus.queue import MessageBus
from deeptutor.tutorbot.channels.base import BaseChannel
from deeptutor.tutorbot.config.schema import Base


class FacebookConfig(Base):
    """Facebook Messenger channel configuration."""

    enabled: bool = False
    page_access_token: str = ""
    verify_token: str = ""
    webhook_port: int = 8080
    webhook_path: str = "/webhook/facebook"


class FacebookChannel(BaseChannel):
    """
    Facebook Messenger channel using Webhooks.
    """

    name = "facebook"
    display_name = "Facebook Messenger"

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        return FacebookConfig().model_dump(by_alias=True)

    def __init__(self, config: Any, bus: MessageBus):
        if isinstance(config, dict):
            config = FacebookConfig.model_validate(config)
        super().__init__(config, bus)
        self.config: FacebookConfig = config
        self._runner: web.AppRunner | None = None
        self._site: web.TCPSite | None = None
        self._session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        """Start the Facebook channel by starting the webhook server."""
        if not self.config.page_access_token or not self.config.verify_token:
            logger.error("Facebook page_access_token or verify_token not configured")
            return

        self._running = True
        self._session = aiohttp.ClientSession()

        app = web.Application()
        app.router.add_get(self.config.webhook_path, self._handle_verification)
        app.router.add_post(self.config.webhook_path, self._handle_messages)

        self._runner = web.AppRunner(app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, "0.0.0.0", self.config.webhook_port)
        await self._site.start()
        logger.info("Facebook Messenger webhook listening on port {}", self.config.webhook_port)

        while self._running:
            await asyncio.sleep(1)

    async def stop(self) -> None:
        """Stop the Facebook channel."""
        self._running = False
        if self._site:
            await self._site.stop()
        if self._runner:
            await self._runner.cleanup()
        if self._session:
            await self._session.close()
        logger.info("Facebook Messenger webhook stopped")

    async def _handle_verification(self, request: web.Request) -> web.Response:
        """Handle Facebook webhook verification."""
        mode = request.query.get("hub.mode")
        token = request.query.get("hub.verify_token")
        challenge = request.query.get("hub.challenge")

        if mode and token:
            if mode == "subscribe" and token == self.config.verify_token:
                logger.info("Facebook webhook verified successfully!")
                return web.Response(text=challenge)
            else:
                return web.Response(status=403, text="Verification token mismatch")
        return web.Response(status=400, text="Missing verification parameters")

    async def _handle_messages(self, request: web.Request) -> web.Response:
        """Handle incoming Facebook messages."""
        try:
            body = await request.json()
        except json.JSONDecodeError:
            return web.Response(status=400, text="Invalid JSON")

        if body.get("object") == "page":
            for entry in body.get("entry", []):
                for webhook_event in entry.get("messaging", []):
                    sender_psid = webhook_event.get("sender", {}).get("id")
                    if webhook_event.get("message"):
                        await self._process_message(sender_psid, webhook_event["message"])

            return web.Response(text="EVENT_RECEIVED")
        return web.Response(status=404, text="Not a page event")

    async def _process_message(self, sender_psid: str, message: dict) -> None:
        """Process a message and forward to the MessageBus."""
        content = message.get("text", "")
        media_paths = []
        
        # Note: In a full implementation, we'd download attachments here.
        if message.get("attachments"):
            for att in message["attachments"]:
                content += f"\n[Attachment: {att.get('type')}]"

        logger.debug("Facebook message from {}: {}", sender_psid, content[:50])

        metadata = {
            "message_id": message.get("mid"),
            "sender_psid": sender_psid
        }

        await self._handle_message(
            sender_id=sender_psid,
            chat_id=sender_psid,
            content=content,
            media=media_paths,
            metadata=metadata
        )

    async def send(self, msg: OutboundMessage) -> None:
        """Send a message through Facebook Messenger."""
        if not self._session:
            return

        url = f"https://graph.facebook.com/v19.0/me/messages?access_token={self.config.page_access_token}"
        
        request_body = {
            "recipient": {
                "id": msg.chat_id
            },
            "message": {
                "text": msg.content
            }
        }
        
        try:
            async with self._session.post(url, json=request_body) as response:
                if response.status != 200:
                    resp_text = await response.text()
                    logger.error("Failed to send Facebook message: {}", resp_text)
        except Exception as e:
            logger.error("Error sending Facebook message: {}", e)
