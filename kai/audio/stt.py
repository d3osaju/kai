"""Speech-to-text functionality."""

import speech_recognition as sr
from typing import Optional


class SpeechRecognizer:
    """Speech recognition using Google Speech Recognition (free, no API key needed)."""
    
    def __init__(self):
        """Initialize speech recognizer."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            print("🎤 Calibrating microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def listen(self, timeout: int = 5, recalibrate: bool = True) -> tuple[Optional[str], str]:
        """Listen for speech and convert to text.
        
        Args:
            timeout: Maximum time to wait for speech
            recalibrate: Whether to recalibrate for ambient noise before listening
            
        Returns:
            Tuple of (recognized_text, status)
            status can be: 'success', 'timeout', 'unclear', 'error'
        """
        try:
            with self.microphone as source:
                # Quick recalibration to filter out any residual audio
                if recalibrate:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            print("🔄 Processing...")
            # Use Google Speech Recognition (free, no API key)
            text = self.recognizer.recognize_google(audio)
            return text, 'success'
            
        except sr.WaitTimeoutError:
            print("⏱️  No speech detected")
            return None, 'timeout'
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None, 'unclear'
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None, 'error'
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, 'error'
