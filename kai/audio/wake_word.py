"""Wake word detection using simple audio pattern matching."""

import pyaudio
import numpy as np
import threading
from typing import Callable
import time


class WakeWordDetector:
    """Simple wake word detector using audio patterns."""
    
    def __init__(self, sensitivity: float = 0.5):
        """Initialize wake word detector.
        
        Args:
            sensitivity: Detection sensitivity (0.0 to 1.0)
        """
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
        
        # Dynamic energy threshold
        self.energy_threshold = 300
        self.ambient_energy = 100
        self.adjustment_count = 0
        
    def start(self, callback: Callable):
        """Start listening for wake word.
        
        Args:
            callback: Function to call when wake word detected
        """
        if self.is_listening:
            return
        
        self.callback = callback
        self.is_listening = True
        
        # Open audio stream
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            # Calibrate for ambient noise
            print("🎤 Calibrating for ambient noise...")
            self._calibrate_ambient_noise()
            
        except Exception as e:
            print(f"Error opening audio stream: {e}")
            return
        
        # Start listening thread
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        
    def _calibrate_ambient_noise(self):
        """Calibrate for ambient noise level."""
        energies = []
        for _ in range(10):
            try:
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                energy = np.sqrt(np.mean(audio_data**2))
                if not np.isnan(energy) and energy > 0:
                    energies.append(energy)
            except:
                pass
        
        if energies:
            self.ambient_energy = np.mean(energies)
            # Set threshold significantly above ambient noise (more strict)
            self.energy_threshold = max(
                self.ambient_energy * (3.0 + self.sensitivity * 4.0),
                300.0  # Higher minimum threshold
            )
            print(f"📊 Ambient: {self.ambient_energy:.1f}, Threshold: {self.energy_threshold:.1f}")
            print(f"💡 Sensitivity: {self.sensitivity:.1f} (lower = less sensitive)")
        else:
            # Fallback if calibration fails
            self.ambient_energy = 100.0
            self.energy_threshold = 400.0  # Higher default
            print(f"⚠️  Calibration failed, using defaults")
        
    def stop(self):
        """Stop listening for wake word."""
        self.is_listening = False
        
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            self.stream = None
        
        if self.thread:
            self.thread.join(timeout=2.0)
            self.thread = None
    
    def _listen_loop(self):
        """Main listening loop."""
        print("🎤 Listening for wake word (say 'Hey Kai' or 'Kai')...")
        print("💡 Tip: Speak clearly and a bit louder than normal")
        
        last_trigger = 0
        cooldown = 3.0  # seconds between triggers
        consecutive_high = 0
        required_consecutive = 5  # Need 5 consecutive high-energy chunks (more strict)
        energy_buffer = []
        buffer_size = 10
        
        while self.is_listening:
            try:
                # Read audio data
                data = self.stream.read(self.chunk, exception_on_overflow=False)
                
                # Convert to numpy array
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                
                # Calculate energy
                energy = np.sqrt(np.mean(audio_data**2))
                
                # Skip invalid readings
                if np.isnan(energy) or energy < 0:
                    continue
                
                # Keep energy buffer for smoothing
                energy_buffer.append(energy)
                if len(energy_buffer) > buffer_size:
                    energy_buffer.pop(0)
                
                # Use smoothed energy
                smoothed_energy = np.mean(energy_buffer) if energy_buffer else energy
                
                # Adaptive threshold adjustment
                self.adjustment_count += 1
                if self.adjustment_count % 100 == 0:
                    # Slowly adjust ambient energy estimate
                    if smoothed_energy < self.energy_threshold * 0.5:
                        self.ambient_energy = self.ambient_energy * 0.95 + smoothed_energy * 0.05
                        self.energy_threshold = max(
                            self.ambient_energy * (3.0 + self.sensitivity * 4.0),
                            300.0  # Higher minimum threshold
                        )
                
                # Voice activity detection with stricter criteria
                current_time = time.time()
                
                # Check if energy is significantly above threshold (not just barely)
                energy_ratio = smoothed_energy / self.energy_threshold
                
                if energy_ratio > 1.5:  # Must be 50% above threshold
                    consecutive_high += 1
                    
                    # Show visual feedback only occasionally
                    if consecutive_high == 1:
                        print(f"🔊 Sound detected (energy: {smoothed_energy:.1f}, ratio: {energy_ratio:.2f})")
                    
                    # Trigger only if we have enough consecutive high-energy chunks
                    # AND the energy is sustained
                    if consecutive_high >= required_consecutive:
                        if current_time - last_trigger > cooldown:
                            # Additional check: verify energy is still high
                            if energy_ratio > 1.3:
                                print("✨ Wake word triggered!")
                                if self.callback:
                                    last_trigger = current_time
                                    consecutive_high = 0
                                    energy_buffer.clear()
                                    self.callback()
                            else:
                                consecutive_high = 0
                else:
                    # Reset if energy drops
                    if consecutive_high > 0:
                        consecutive_high = 0
                        
            except Exception as e:
                if self.is_listening:
                    print(f"Error in wake word detection: {e}")
                break
    
    def __del__(self):
        """Cleanup on deletion."""
        self.stop()
        try:
            self.audio.terminate()
        except:
            pass
