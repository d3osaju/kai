"""Hotword detection for wake word."""

import pyaudio
import struct
import math
from typing import Callable, Optional
import threading


class HotwordDetector:
    """Simple hotword detector using audio energy and pattern matching."""
    
    def __init__(self, wake_words: list = None, sensitivity: float = 0.5):
        """Initialize hotword detector.
        
        Args:
            wake_words: List of wake words to detect
            sensitivity: Detection sensitivity (0.0 to 1.0)
        """
        self.wake_words = wake_words or ["hey kai", "kai"]
        self.sensitivity = sensitivity
        self.is_listening = False
        self.callback = None
        
        # Audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None
        
    def start(self, callback: Callable):
        """Start listening for hotword.
        
        Args:
            callback: Function to call when hotword detected
        """
        if self.is_listening:
            return
        
        self.callback = callback
        self.is_listening = True
        
        # Open audio stream
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        # Start listening thread
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop listening for hotword."""
        self.is_listening = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
    
    def _listen_loop(self):
        """Main listening loop."""
        print("🎤 Listening for wake word...")
        
        while self.is_listening:
            try:
                # Read audio data
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                
                # Calculate audio energy
                energy = self._calculate_energy(data)
                
                # Simple threshold-based detection
                # In a real implementation, you'd use a proper hotword model
                if energy > 1000 * self.sensitivity:
                    if self.callback:
                        self.callback()
                        
            except Exception as e:
                print(f"Error in hotword detection: {e}")
                break
    
    def _calculate_energy(self, data: bytes) -> float:
        """Calculate audio energy level.
        
        Args:
            data: Audio data bytes
            
        Returns:
            Energy level
        """
        # Convert bytes to integers
        count = len(data) / 2
        format_str = "%dh" % count
        shorts = struct.unpack(format_str, data)
        
        # Calculate RMS energy
        sum_squares = sum(s ** 2 for s in shorts)
        rms = math.sqrt(sum_squares / count)
        
        return rms
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
        self.audio.terminate()
