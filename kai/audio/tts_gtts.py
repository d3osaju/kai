"""Better text-to-speech using Google TTS."""

from gtts import gTTS
import tempfile
import os
import subprocess
import re
import threading
from typing import Optional


class GoogleTTS:
    """Natural-sounding text-to-speech using Google TTS."""
    
    def __init__(self, lang: str = 'en', slow: bool = False, speed: float = 1.0, audio_device: str = None):
        """Initialize Google TTS.
        
        Args:
            lang: Language code (en, es, fr, etc.)
            slow: Speak slowly (overrides speed if True)
            speed: Playback speed multiplier (0.5 = half speed, 2.0 = double speed)
                   1.0 = normal, 1.2 = 20% faster, 1.5 = 50% faster
            audio_device: ALSA audio device (e.g., 'hw:0,3' or 'default')
        """
        self.lang = lang
        self.slow = slow
        self.speed = speed
        self.audio_device = audio_device or 'default'
        self.temp_files = []
        self.current_process = None
        self.is_speaking = False
        
    def speak(self, text: str, wait: bool = True, stream: bool = True):
        """Speak the given text with natural voice.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
            stream: Whether to stream sentence-by-sentence for faster response
        """
        self.is_speaking = True
        
        # For long text, stream sentence by sentence with parallel processing
        if stream and len(text) > 100:
            sentences = self._split_sentences(text)
            
            # Process sentences with pipeline: generate next while playing current
            import queue
            import threading
            
            audio_queue = queue.Queue(maxsize=2)  # Buffer 2 audio files
            
            def generate_audio():
                """Generate audio files in background thread."""
                for sentence in sentences:
                    if not self.is_speaking:
                        break
                    if sentence.strip():
                        audio_file = self._generate_audio_file(sentence.strip())
                        if audio_file and self.is_speaking:
                            audio_queue.put(audio_file)
                audio_queue.put(None)  # Signal end
            
            # Start generation thread
            gen_thread = threading.Thread(target=generate_audio, daemon=True)
            gen_thread.start()
            
            # Play audio files as they're generated
            while self.is_speaking:
                try:
                    audio_file = audio_queue.get(timeout=10)
                    if audio_file is None:  # End signal
                        break
                    if self.is_speaking:
                        self._play_audio_file(audio_file)
                except queue.Empty:
                    break
            
            gen_thread.join(timeout=1)
        else:
            self._speak_chunk(text, wait=wait)
        
        self.is_speaking = False
    
    def _split_sentences(self, text: str) -> list:
        """Split text into sentences for streaming.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return sentences
    
    def _generate_audio_file(self, text: str) -> Optional[str]:
        """Generate audio file for text without playing it.
        
        Args:
            text: Text to convert to audio
            
        Returns:
            Path to audio file, or None if generation failed
        """
        if not self.is_speaking:
            return None
            
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            self.temp_files.append(temp_file.name)
            
            print(f"[DEBUG] Generating audio: {temp_file.name}")
            tts.save(temp_file.name)
            
            if not self.is_speaking:
                return None
            
            # Apply speed adjustment if needed
            if self.speed != 1.0 and not self.slow:
                speed_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                speed_file.close()
                self.temp_files.append(speed_file.name)
                
                result = subprocess.run(['sox', temp_file.name, speed_file.name, 'tempo', str(self.speed)],
                             capture_output=True, text=True)
                if result.returncode != 0:
                    return temp_file.name
                return speed_file.name
            
            return temp_file.name
            
        except Exception as e:
            print(f"TTS Generation Error: {e}")
            return None
    
    def _play_audio_file(self, audio_file: str):
        """Play a pre-generated audio file.
        
        Args:
            audio_file: Path to audio file to play
        """
        if not self.is_speaking or not audio_file:
            return
            
        try:
            print(f"[DEBUG] Playing: {audio_file}")
            
            mpg123_cmd = ['/usr/bin/mpg123', '-a', self.audio_device, '-q', audio_file]
            
            self.current_process = subprocess.Popen(mpg123_cmd,
                                                   stdout=subprocess.DEVNULL,
                                                   stderr=subprocess.PIPE)
            self.current_process.communicate()
            self.current_process = None
            
            self._cleanup_old_files()
            
        except Exception as e:
            print(f"Playback Error: {e}")
    
    def _speak_chunk(self, text: str, wait: bool = True):
        """Speak a single chunk of text.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        # Check if we should stop before generating audio
        if not self.is_speaking:
            return
            
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=self.lang, slow=self.slow)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            self.temp_files.append(temp_file.name)
            
            print(f"[DEBUG] Saving TTS to: {temp_file.name}")
            tts.save(temp_file.name)
            print(f"[DEBUG] TTS file saved, size: {os.path.getsize(temp_file.name)} bytes")
            
            # Check again before processing
            if not self.is_speaking:
                return
            
            # Play the audio file with speed control
            # mpg123 doesn't support speed directly, so we use sox for speed control
            if self.speed != 1.0 and not self.slow:
                # Use sox to adjust speed
                speed_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                speed_file.close()
                self.temp_files.append(speed_file.name)
                
                print(f"[DEBUG] Adjusting speed with sox...")
                result = subprocess.run(['sox', temp_file.name, speed_file.name, 'tempo', str(self.speed)],
                             capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"[DEBUG] Sox error: {result.stderr}")
                    playback_file = temp_file.name
                else:
                    playback_file = speed_file.name
            else:
                playback_file = temp_file.name
            
            # Check one more time before playing
            if not self.is_speaking:
                return
            
            # Play the audio
            print(f"[DEBUG] Playing audio with mpg123: {playback_file} on device: {self.audio_device}")
            
            # Build mpg123 command with audio device
            mpg123_cmd = ['/usr/bin/mpg123', '-a', self.audio_device, '-q', playback_file]
            
            if wait:
                # Use full path to mpg123
                self.current_process = subprocess.Popen(mpg123_cmd,
                                                       stdout=subprocess.DEVNULL,
                                                       stderr=subprocess.PIPE)
                stderr_output = self.current_process.communicate()[1]
                if self.current_process.returncode and self.current_process.returncode != 0:
                    print(f"[DEBUG] mpg123 error: {stderr_output.decode() if stderr_output else 'Unknown error'}")
                self.current_process = None
            else:
                self.current_process = subprocess.Popen(mpg123_cmd,
                                                       stdout=subprocess.DEVNULL,
                                                       stderr=subprocess.DEVNULL)
            
            # Clean up old temp files
            self._cleanup_old_files()
            
        except FileNotFoundError as e:
            print(f"Error: Required tool not found: {e}")
            print("Install with: sudo apt-get install mpg123 sox")
        except Exception as e:
            print(f"TTS Error: {e}")
            import traceback
            traceback.print_exc()
    
    def _cleanup_old_files(self):
        """Clean up old temporary files."""
        # Keep only the last 5 files
        while len(self.temp_files) > 5:
            old_file = self.temp_files.pop(0)
            try:
                if os.path.exists(old_file):
                    os.remove(old_file)
            except:
                pass
    
    def stop(self):
        """Stop current speech."""
        self.is_speaking = False
        try:
            if self.current_process:
                self.current_process.terminate()
                self.current_process.wait(timeout=1)
                self.current_process = None
        except:
            pass
        
        # Fallback: kill all mpg123 processes
        try:
            subprocess.run(['/usr/bin/pkill', 'mpg123'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
        except:
            pass
    
    def cleanup(self):
        """Clean up all temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_files = []
    
    def __del__(self):
        """Cleanup on deletion."""
        self.cleanup()
