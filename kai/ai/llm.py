"""LLM integration for Kai."""

import ollama
from typing import Optional, Dict, Any


class LLMEngine:
    """Handles LLM interactions using Ollama."""
    
    def __init__(self, model: str = "llama3.2:3b"):
        """Initialize LLM engine.
        
        Args:
            model: Model name to use
        """
        self.model = model
        self.client = ollama.Client()
        self.default_system_prompt = """You are Kai, a helpful voice assistant for Linux users.

CRITICAL RULES FOR VOICE RESPONSES:
- Keep responses SHORT and CONVERSATIONAL (2-3 sentences max)
- Speak naturally like a human, not like written text
- NO markdown formatting (no *, **, _, `, etc.)
- NO bullet points or numbered lists
- NO code blocks or technical formatting
- Use simple, clear language
- If listing items, use "first", "second", "also" instead of bullets
- Be friendly and concise

Example GOOD response: "Sure! To update your system, open a terminal and run sudo apt update, then sudo apt upgrade. That will update all your packages."

Example BAD response: "Here's how to update:\n* First, run `sudo apt update`\n* Then run `sudo apt upgrade`\n**Note:** This requires admin privileges"

Remember: You're SPEAKING to someone, not writing documentation."""
        
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response from LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated response text
        """
        messages = []
        
        # Use default system prompt if none provided
        if system_prompt is None:
            system_prompt = self.default_system_prompt
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat(self, messages: list) -> str:
        """Continue a conversation.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Generated response text
        """
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"Error in chat: {str(e)}"
