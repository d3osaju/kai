"""General query plugin implementation."""

from kai.plugins.base import Plugin
from kai.core.intent import Intent
from kai.ai.llm import LLMEngine


class GeneralQueryPlugin(Plugin):
    """Plugin for handling general queries using LLM."""
    
    def __init__(self):
        super().__init__(
            name="general_query",
            version="1.0.0",
            intents=["general_query"]
        )
        self.llm = None
        
    async def handle_intent(self, intent: Intent) -> str:
        """Handle general query intents.
        
        Args:
            intent: Intent to handle
            
        Returns:
            Response text
        """
        # Initialize LLM lazily
        if self.llm is None:
            try:
                self.llm = LLMEngine(model="llama3.2:3b")
            except Exception as e:
                return f"Error initializing LLM: {str(e)}. Make sure Ollama is running and the model is downloaded."
        
        # Create system prompt optimized for voice interaction
        system_prompt = """You are Kai, a friendly voice assistant for Linux users.

VOICE RESPONSE RULES (CRITICAL):
- Keep responses SHORT (2-3 sentences maximum)
- Speak naturally like talking to a friend
- NEVER use markdown, asterisks, or formatting symbols
- NO bullet points, numbered lists, or code blocks
- If listing things, say "first", "second", "also" naturally
- Be conversational and helpful
- Get to the point quickly

Example: "To check disk space, just run d-f dash h in your terminal. That shows you how much space is used and available on each drive."

NOT: "Here's how:\n* Run `df -h`\n* This shows disk usage\n**Note:** Requires terminal access"

Remember: Someone is LISTENING to you speak, not reading text."""
        
        try:
            response = self.llm.generate(
                prompt=intent.raw_text,
                system_prompt=system_prompt
            )
            return response
        except Exception as e:
            return f"Error processing query: {str(e)}"
