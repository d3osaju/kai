"""Main assistant class."""

import asyncio
from typing import Optional
from kai.core.config import Config
from kai.core.intent import IntentRecognizer
from kai.plugins.manager import PluginManager


class Assistant:
    """Main Kai assistant class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the assistant.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = Config(config_path)
        self.intent_recognizer = IntentRecognizer(self.config)
        self.plugin_manager = PluginManager(self.config)
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 exchanges
        
    async def initialize(self):
        """Initialize async components."""
        await self.plugin_manager.load_plugins()
        
    def query(self, text: str) -> str:
        """Process a text query.
        
        Args:
            text: User query text
            
        Returns:
            Response text
        """
        return asyncio.run(self.async_query(text))
        
    async def async_query(self, text: str) -> str:
        """Process a text query asynchronously.
        
        Args:
            text: User query text
            
        Returns:
            Response text
        """
        # Recognize intent
        intent = await self.intent_recognizer.recognize(text)
        
        # Execute via plugin with conversation history
        response = await self.plugin_manager.execute_intent(intent, self.conversation_history)
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": text
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Trim history if too long
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
        
        return response
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_history(self):
        """Get conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history.copy()
