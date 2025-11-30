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
        """Recognize intent from text using LLM.
        
        Args:
            text: User input text
            
        Returns:
            Recognized intent
        """
        # Use LLM to classify intent
        from kai.ai.llm import LLMEngine
        
        # Get model from config
        model = self.config.get("models.llm", "llama3.2:3b")
        
        # Get available intents dynamically
        valid_intents = ["install_package", "execute_command", "launch_app", "close_app", "general_query"]
        
        try:
            llm = LLMEngine(model=model)
            
            # Build intent descriptions dynamically
            intent_descriptions = "\n".join([
                f"{i+1}. {intent} - {self._get_intent_description(intent)}"
                for i, intent in enumerate(valid_intents)
            ])
            
            intent_prompt = f"""Analyze this user request and classify it into ONE of these intents:

{intent_descriptions}

User request: "{text}"

Respond with ONLY the intent name (one word), nothing else."""

            intent_name = llm.generate(
                intent_prompt, 
                system_prompt="You are an intent classifier. Respond with only the intent name."
            ).strip().lower()
            
            if intent_name not in valid_intents:
                intent_name = self._fallback_intent(text)
            
            # Extract entities based on intent
            entities = {}
            if intent_name in ["launch_app", "close_app"]:
                entities["app"] = self._extract_app_name(text)
            
            return Intent(
                name=intent_name,
                confidence=0.9,
                entities=entities,
                raw_text=text
            )
            
        except Exception as e:
            return self._fallback_intent_obj(text)
    
    def _get_intent_description(self, intent: str) -> str:
        """Get description for an intent.
        
        Args:
            intent: Intent name
            
        Returns:
            Intent description
        """
        descriptions = {
            "install_package": "User wants to install software or package",
            "execute_command": "User wants to run a specific command",
            "launch_app": "User wants to open an application",
            "close_app": "User wants to close an application",
            "general_query": "User is asking a question or needs information"
        }
        return descriptions.get(intent, "Unknown intent")
    
    def _fallback_intent(self, text: str) -> str:
        """Fallback keyword-based intent recognition.
        
        Args:
            text: User input text
            
        Returns:
            Intent name
        """
        text_lower = text.lower()
        
        # Get keywords from config or use defaults
        install_keywords = self.config.get("intents.install_keywords", ["install", "download", "get"])
        execute_keywords = self.config.get("intents.execute_keywords", ["run command", "execute", "run this"])
        launch_keywords = self.config.get("intents.launch_keywords", ["open", "launch"])
        close_keywords = self.config.get("intents.close_keywords", ["close", "quit", "kill"])
        
        if any(keyword in text_lower for keyword in install_keywords):
            return "install_package"
        elif any(keyword in text_lower for keyword in execute_keywords):
            return "execute_command"
        elif any(keyword in text_lower for keyword in launch_keywords):
            return "launch_app"
        elif any(keyword in text_lower for keyword in close_keywords):
            return "close_app"
        else:
            return "general_query"
    
    def _fallback_intent_obj(self, text: str) -> Intent:
        """Create Intent object using fallback.
        
        Args:
            text: User input text
            
        Returns:
            Intent object
        """
        intent_name = self._fallback_intent(text)
        entities = {}
        
        if intent_name in ["launch_app", "close_app"]:
            entities["app"] = self._extract_app_name(text)
        
        return Intent(
            name=intent_name,
            confidence=0.7,
            entities=entities,
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
