"""Base plugin class."""

from abc import ABC, abstractmethod
from typing import List
from kai.core.intent import Intent


class Plugin(ABC):
    """Base class for all Kai plugins."""
    
    def __init__(self, name: str, version: str = "1.0.0", intents: List[str] = None):
        """Initialize plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
            intents: List of intent names this plugin handles
        """
        self.name = name
        self.version = version
        self.intents = intents or []
        
    @abstractmethod
    async def handle_intent(self, intent: Intent) -> str:
        """Handle an intent.
        
        Args:
            intent: Intent to handle
            
        Returns:
            Response text
        """
        pass
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this plugin can handle the intent.
        
        Args:
            intent: Intent to check
            
        Returns:
            True if plugin can handle this intent
        """
        return intent.name in self.intents
