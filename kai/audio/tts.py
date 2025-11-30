"""Text-to-speech functionality."""

import pyttsx3
from typing import Optional


class TextToSpeech:
    """Text-to-speech engine using pyttsx3."""
    
    def __init__(self, rate: int = 175, volume: float = 1.0):
        """Initialize TTS engine.
        
        Args:
            rate: Speech rate (words per minute)
            volume: Volume level (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Try to set a better voice
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'f' in voice.id.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def speak(self, text: str, wait: bool = True):
        """Speak the given text.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def stop(self):
        """Stop current speech."""
        try:
            self.engine.stop()
        except:
            pass
    
    def set_rate(self, rate: int):
        """Set speech rate.
        
        Args:
            rate: Words per minute
        """
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume level.
        
        Args:
            volume: Volume (0.0 to 1.0)
        """
        self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """List available voices."""
        voices = self.engine.getProperty('voices')
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name} ({voice.id})")
    
    def set_voice(self, voice_id: str):
        """Set voice by ID.
        
        Args:
            voice_id: Voice ID
        """
        self.engine.setProperty('voice', voice_id)
