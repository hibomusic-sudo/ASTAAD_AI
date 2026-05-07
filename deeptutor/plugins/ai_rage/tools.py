import json
import os
from typing import Any
from deeptutor.core.tool_protocol import BaseTool, ToolDefinition, ToolParameter, ToolResult

class GetDailyLessonTool(BaseTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="get_daily_lesson",
            description="Fetch the curriculum, instructions, and resources for a specific day (1-28) of the AI course.",
            parameters=[
                ToolParameter(
                    name="day_number",
                    type="integer",
                    description="The day number of the course (e.g., 1 for Day 1, 15 for Day 15). Must be between 1 and 28.",
                    required=True
                )
            ]
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        day_number = kwargs.get("day_number")
        
        if not isinstance(day_number, int) or day_number < 1 or day_number > 28:
            return ToolResult(
                content=f"Error: Invalid day number '{day_number}'. Please request a day between 1 and 28.",
                success=False
            )
            
        # Load the curriculum JSON file
        curriculum_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "tutorbot", "ai_rage", "curriculum_28_days.json")
        try:
            with open(curriculum_path, 'r', encoding='utf-8') as f:
                curriculum_data = json.load(f)
        except Exception as e:
            return ToolResult(
                content=f"Error loading curriculum data: {str(e)}",
                success=False
            )
            
        day_key = str(day_number)
        if day_key not in curriculum_data:
            return ToolResult(
                content=f"Notice: Day {day_number} is not explicitly defined in the curriculum yet.",
                success=True
            )
            
        lesson = curriculum_data[day_key]
        
        title_val = lesson.get("title", "Magac la'aan")
        desc_val = lesson.get("description", "")
        link_val = lesson.get("resource_link", "Link lama gelin")
        
        content = (
            f"Halkan waa casharka loogu talagalay Maalinta {day_number}aad:\n\n"
            f"**Cinwaanka:** {title_val}\n"
            f"**Faahfaahin:** {desc_val}\n"
            f"**Linkiga Casharka (Resource):** {link_val}\n\n"
            "Instruct the student to review the resource and ask any questions they have. Use Somali."
        )
        
        return ToolResult(content=content, success=True)


class CommunityLinksTool(BaseTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="send_community_links",
            description="Send community links (WhatsApp, Loom, etc.) as interactive Telegram buttons. Call this when a student asks for links or graduates from a quiz.",
            parameters=[
                ToolParameter(
                    name="course_name",
                    type="string",
                    description="Optional specific course to highlight. If 'all', shows all links.",
                    required=False,
                    default="all"
                )
            ]
        )

    async def execute(self, **kwargs: Any) -> ToolResult:
        course_name = kwargs.get("course_name", "all")
        
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
        
        # In DeepTutor Tools, they just return ToolResult. If we want metadata returned,
        # we can put it in the ToolResult.metadata. The LLM won't see it, but the capability or pipeline
        # could see it? Wait, how does a ToolResult metadata get to the Telegram bot?
        # The tool result is just added to context as a function message. It doesn't stream back to the user automatically.
        # Wait, if we want to stream content directly from the tool, we need the `stream` object, which is NOT passed to `execute(**kwargs)`! `execute` only gets `kwargs` (parameters).
        
        # If we can't stream directly, the LLM will just output its own message. But we want the LLM's NEXT message to have the reply_markup.
        # DeepTutor streams use `stream.content()`. The simplest hack is to return a special tag in the text content, OR
        # just have the bot output markdown links normally if the custom tool fails.
        return ToolResult(
            content="Tool executed. The user expects links now. Output the links as beautifully formatted markdown if needed.",
            metadata={"reply_markup": reply_markup}
        )
