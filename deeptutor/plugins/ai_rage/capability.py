"""AI Rage Capability Plugin."""

from deeptutor.core.capability_protocol import BaseCapability, CapabilityManifest
from deeptutor.core.context import UnifiedContext
from deeptutor.core.stream_bus import StreamBus
from deeptutor.agents.chat.agentic_pipeline import AgenticChatPipeline

class AIRageCapability(BaseCapability):
    manifest = CapabilityManifest(
        name="ai_rage",
        description="AI Rage Learning Companion (Somali)",
        stages=["thinking", "acting", "observing", "responding"],
        tools_used=["rag", "manage_schedule", "manage_classwork", "web_search", "code_execution", "send_community_links"],
    )

    async def run(self, context: UnifiedContext, stream: StreamBus) -> None:
        # Override the user message to inject Somali language instructions and persona.
        instruction = (
            "Waxaad tahay 'AI Rage', oo ah macalin AI ah oo ku hadla afka Soomaaliga. "
            "Waxaad ardayda u dhigtaa casharo ku saabsan Vibe coding, iyo basic programming.\n"
            "Waxaad adeegsan kartaa qalabka (tools) si aad u hesho macluumaad dheeraad ah (RAG) "
            "ama aad u maamusho jadwalka (schedule) iyo shaqada fasalada.\n"
            "MUHIIM: Marka ardaygu dhammeeyo Koorada (Course), sii Imtixaan (Quiz). Marka ay baastaan ama marka ay ku weydiiyaan links-ka (Menu), "
            "waa inaad KELIYA isticmaashaa tool-ka `send_community_links` si aad ugu dirto badhamada (Interactive Buttons). "
            "Ha qorin links-ka adigoo text caadi ah isticmaalaya, isticmaal tool-kaas markasta!\n"
            "Haddii lagu weydiiyo su'aal, ku jawaab si xushmad leh oo ku bixi sharaxaad faahfaahsan.\n\n"
            f"Su'aasha ardayga: {context.user_message.content}"
        )
        
        context.user_message.content = instruction
        
        # Ensure our tools are enabled
        for tool in self.manifest.tools_used:
            if tool not in context.enabled_tools:
                context.enabled_tools.append(tool)
        
        # Run the standard agentic pipeline
        pipeline = AgenticChatPipeline(language="en")
        await pipeline.run(context, stream)
