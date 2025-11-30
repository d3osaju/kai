"""Intent recognition."""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from kai.core.config import Config


@dataclass
class Intent:
    """Represents a recognized user intent."""
    
    name: str
    confidence: float
    entities: Dict[str, Any]
    raw_text: str


class IntentRecognizer:
    """Recognizes user intents from text."""
    
    def __init__(self, config: Config):
        """Initialize intent recognizer.
        
        Args:
            config: Configuration object
        """
        self.config = config
        
    async def recognize(self, text: str) -> Intent:
        """Recognize intent from text.
        
        Args:
            text: User input text
            
        Returns:
            Recognized intent
        """
        # Simple keyword-based recognition
        text_lower = text.lower()
        
        # System control intents
        if any(word in text_lower for word in ["open", "launch", "start"]):
            app_name = self._extract_app_name(text)
            if app_name:
                return Intent(
                    name="launch_app",
                    confidence=0.8,
                    entities={"app": app_name},
                    raw_text=text
                )
        
        if any(word in text_lower for word in ["close", "quit", "kill"]):
            app_name = self._extract_app_name(text)
            if app_name:
                return Intent(
                    name="close_app",
                    confidence=0.8,
                    entities={"app": app_name},
                    raw_text=text
                )
        
        # Default to general query (will use LLM)
        return Intent(
            name="general_query",
            confidence=0.9,
            entities={},
            raw_text=text
        )
    
    def _extract_app_name(self, text: str) -> Optional[str]:
        """Extract application name from text.
        
        Args:
            text: Input text
            
        Returns:
            Application name if found
        """
        # Simple extraction - look for word after action verb
        words = text.lower().split()
        action_words = ["open", "launch", "start", "close", "quit", "kill"]
        
        for i, word in enumerate(words):
            if word in action_words and i + 1 < len(words):
                return words[i + 1]
        
        return None
