"""Command-line interface for Kai."""

import click
import asyncio
import re
from rich.console import Console
from kai.core.assistant import Assistant

console = Console()


def _clean_for_speech(text: str) -> str:
    """Clean text for natural speech output.
    
    Removes markdown formatting, bullet points, and other text artifacts
    that don't sound natural when spoken.
    
    Args:
        text: Raw text with possible markdown formatting
        
    Returns:
        Cleaned text suitable for TTS
    """
    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic*
    text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_
    
    # Remove markdown headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Convert bullet points to natural speech
    text = re.sub(r'^\s*[\*\-\+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Remove code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\n\s*\n', '. ', text)  # Multiple newlines -> period
    text = re.sub(r'\n', ' ', text)         # Single newlines -> space
    text = re.sub(r'\s+', ' ', text)        # Multiple spaces -> single space
    
    # Clean up punctuation
    text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([.,!?])\s*([.,!?])', r'\1', text)  # Remove duplicate punctuation
    
    return text.strip()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """Kai - Open-source AI assistant for Linux."""
    pass


@main.command()
@click.argument("query", nargs=-1)
def query(query):
    """Send a query to Kai."""
    if not query:
        console.print("[red]Please provide a query[/red]")
        return
    
    query_text = " ".join(query)
    
    console.print(f"[cyan]You:[/cyan] {query_text}")
    
    assistant = Assistant()
    asyncio.run(assistant.initialize())
    response = assistant.query(query_text)
    
    console.print(f"[green]Kai:[/green] {response}")


@main.command()
def start():
    """Start Kai in interactive mode."""
    console.print("[bold green]Kai Assistant[/bold green]")
    console.print("Type 'exit' or 'quit' to stop\n")
    
    assistant = Assistant()
    asyncio.run(assistant.initialize())
    
    while True:
        try:
            user_input = console.input("[cyan]You:[/cyan] ")
            
            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if not user_input.strip():
                continue
            
            response = assistant.query(user_input)
            console.print(f"[green]Kai:[/green] {response}\n")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}\n")


@main.command()
@click.option('--sensitivity', '-s', default=0.3, type=float, help='Wake word sensitivity (0.0-1.0, lower=less sensitive)')
@click.option('--speak/--no-speak', default=True, help='Enable/disable voice responses')
@click.option('--speed', default=1.2, type=float, help='Voice speed (1.0=normal, 1.5=faster, 2.0=very fast)')
@click.option('--volume', '-v', default=100, type=int, help='Volume level (0-100, default=100)')
def voice(sensitivity, speak, speed, volume):
    """Start Kai in voice mode with wake word detection."""
    console.print("[bold green]Kai Voice Assistant[/bold green]")
    console.print("Say 'Hey Kai' or 'Kai' to activate")
    console.print(f"Sensitivity: {sensitivity}")
    console.print(f"Voice speed: {speed}x")
    console.print(f"Volume: {volume}%")
    console.print(f"Voice responses: {'Enabled' if speak else 'Disabled'}")
    console.print("Press Ctrl+C to stop\n")
    
    try:
        from kai.audio.stt import SpeechRecognizer
        from kai.audio.wake_word import WakeWordDetector
        from kai.audio.tts_gtts import GoogleTTS
        import subprocess
    except ImportError as e:
        console.print(f"[red]Error:[/red] Missing audio dependencies")
        console.print("Install with: pip install SpeechRecognition pyaudio numpy gTTS")
        return
    
    console.print("[cyan]Initializing Kai...[/cyan]")
    assistant = Assistant()
    asyncio.run(assistant.initialize())
    
    console.print("[cyan]Initializing speech recognition...[/cyan]")
    stt = SpeechRecognizer()
    
    # Initialize TTS if enabled
    tts = None
    if speak:
        console.print("[cyan]Initializing text-to-speech (Google TTS)...[/cyan]")
        try:
            tts = GoogleTTS(lang='en', slow=False, speed=speed)
            # Set volume using amixer if available
            try:
                subprocess.run(['amixer', 'sset', 'Master', f'{volume}%'], 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
            console.print(f"[green]✓ Natural voice responses enabled ({speed}x speed, {volume}% volume)[/green]")
        except Exception as e:
            console.print(f"[yellow]Warning: TTS initialization failed: {e}[/yellow]")
            console.print("[yellow]Continuing without voice responses[/yellow]")
            tts = None
    
    def on_wake_word():
        """Handle wake word detection."""
        import time
        
        console.print("\n[bold green]✓ Wake word detected![/bold green]")
        
        # Speak friendly acknowledgment and WAIT for it to finish
        if tts:
            tts.speak("Yes?", wait=True)
        
        # Small delay to ensure audio output is completely done
        time.sleep(0.3)
        
        # Enter conversation mode - stay awake for follow-up questions
        silence_count = 0
        unclear_count = 0
        max_silence = 1  # Exit after 1 silent attempt (5 seconds)
        max_unclear = 2  # Exit after 2 unclear attempts (avoid loops)
        
        while silence_count < max_silence and unclear_count < max_unclear:
            # Listen for command
            console.print("[dim]🎤 Listening...[/dim]")
            text, status = stt.listen(timeout=5, recalibrate=False)
            
            if status == 'success' and text:
                silence_count = 0  # Reset silence counter
                unclear_count = 0  # Reset unclear counter
                console.print(f"[cyan]You:[/cyan] {text}")
                console.print("[dim]🔄 Processing...[/dim]")
                response = assistant.query(text)
                console.print(f"[green]Kai:[/green] {response}\n")
                
                # Clean response for speech (remove markdown formatting)
                speech_response = _clean_for_speech(response)
                
                # Speak the response with keyboard interrupt
                if tts:
                    console.print("[dim]🔊 Speaking... (press SPACE to interrupt)[/dim]")
                    
                    # Start speaking in a thread
                    import threading
                    import select
                    import sys
                    import termios
                    import tty
                    
                    speak_thread = threading.Thread(target=lambda: tts.speak(speech_response, wait=True))
                    speak_thread.start()
                    
                    # Monitor for keyboard interrupt
                    interrupted = False
                    old_settings = termios.tcgetattr(sys.stdin)
                    try:
                        tty.setcbreak(sys.stdin.fileno())
                        while speak_thread.is_alive():
                            if select.select([sys.stdin], [], [], 0.1)[0]:
                                key = sys.stdin.read(1)
                                if key == ' ':  # Space bar
                                    console.print("\n[yellow]⚠️  Interrupted![/yellow]")
                                    tts.stop()
                                    interrupted = True
                                    break
                    finally:
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    
                    speak_thread.join(timeout=1)
                    
                    if interrupted:
                        console.print("[dim]💬 Continue speaking...[/dim]")
                        time.sleep(0.3)
                        continue  # Skip delay and listen immediately
                
                # Small delay before listening again
                time.sleep(0.5)
                console.print("[dim]💬 Still listening... (say something or wait to sleep)[/dim]")
            elif status == 'unclear':
                # Could hear something but couldn't understand
                unclear_count += 1
                if unclear_count < max_unclear:
                    console.print("[yellow]🤔 Sorry, I didn't catch that.[/yellow]")
                    if tts:
                        tts.speak("Sorry, I didn't catch that", wait=True)
                    # Wait longer to avoid picking up our own voice
                    time.sleep(1.0)
                else:
                    console.print("[yellow]🤔 Having trouble understanding. Let me go to sleep.[/yellow]")
                    if tts:
                        tts.speak("Having trouble understanding", wait=True)
                    time.sleep(0.5)
            elif status == 'timeout':
                # True silence - count it
                silence_count += 1
                if silence_count < max_silence:
                    console.print(f"[dim]⏸️  Silence detected ({silence_count}/{max_silence})[/dim]")
                    time.sleep(0.5)
            else:
                # Error - don't count as silence, just try again
                time.sleep(0.5)
        
        # Exit conversation mode
        console.print("[yellow]😴 Going to sleep...[/yellow]")
        if tts:
            tts.speak("Going to sleep", wait=True)
        time.sleep(0.3)
        console.print("[dim]Listening for wake word...[/dim]")
    
    # Start wake word detection
    console.print("[cyan]Starting wake word detection...[/cyan]\n")
    detector = WakeWordDetector(sensitivity=sensitivity)
    
    try:
        detector.start(on_wake_word)
        
        # Keep running
        while True:
            import time
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping voice mode...[/yellow]")
        detector.stop()
        if tts:
            tts.stop()
        console.print("[green]Goodbye![/green]")


@main.command()
def setup():
    """Setup Kai configuration."""
    console.print("[bold]Setting up Kai...[/bold]")
    
    # Initialize config
    assistant = Assistant()
    
    console.print(f"[green]✓[/green] Configuration created at: {assistant.config.config_path}")
    console.print("[green]✓[/green] Kai is ready to use!")
    console.print("\nRun 'kai start' to begin")


@main.command()
def settings():
    """Launch settings GUI."""
    from kai.gui.app import launch_gui
    console.print("[green]Opening Kai settings...[/green]")
    launch_gui()


if __name__ == "__main__":
    main()
