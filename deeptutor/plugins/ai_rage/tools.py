import json
from deeptutor.core.tool_protocol import BaseTool, ToolManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus

class CommunityLinksTool(BaseTool):
    manifest = ToolManifest(
        name="send_community_links",
        description="Send community links (WhatsApp, Loom, etc.) as interactive Telegram buttons. Call this when a student asks for links or graduates from a quiz.",
        parameters={
            "type": "object",
            "properties": {
                "course_name": {
                    "type": "string",
                    "description": "Optional specific course to highlight. If 'all', shows all links."
                }
            }
        }
    )

    async def execute(
        self,
        arguments: dict,
        context: UnifiedContext,
        stream: StreamBus,
        stage: str = "observing"
    ) -> str:
        course_name = arguments.get("course_name", "all")
        
        # Build the Inline Keyboard
        reply_markup = {
            "inline_keyboard": [
                [{"text": "🤖 AI BOT (Automation) 4 Days", "url": "https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM"}],
                [{"text": "🌍 AI-Whatsapp Community", "url": "https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq"}],
                [{"text": "🎬 AI Video Editing", "url": "https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq"}],
                [{"text": "📚 Fasalka Barashada AI", "url": "https://chat.whatsapp.com/CEDDPttA5a4K6ZkQsDp4ah"}],
                [{"text": "📹 Loom Workspace (Nala Shaqee)", "url": "https://loom.com/invite/f510cb6235b947838f247150307bfbeb"}],
                [
                    {"text": "🎵 Himbomusic", "url": "https://himbomusic.com"},
                    {"text": "🔬 Somalilab", "url": "https://somalilab.com"}
                ],
                [{"text": "🌐 Somalibotmaster", "url": "https://somalibotmaster.net"}]
            ]
        }
        
        # We need to send this metadata out so Telegram catches it.
        # Since this tool executes inside the agent loop, we can just stream a raw JSON payload
        # that the agent will interpret, BUT wait, the metadata goes out when the AGENT streams content.
        # DeepTutor streams use `await stream.content(..., metadata={})`. 
        # By streaming this directly to the bus, it will bypass the LLM and show up in Telegram immediately!
        
        message = "Hooyo/Walaal, halkan waxaa ah links-ka muhiimka ah ee Fasallada iyo Bulshada AI Rage! Fadlan ku dhufo badhamada (buttons) hoose si aad ugu biirto:"
        
        await stream.content(
            message,
            source=self.name,
            metadata={"reply_markup": reply_markup}
        )
        
        return "Successfully sent interactive buttons to the user. Do not output the links again as plain text."
