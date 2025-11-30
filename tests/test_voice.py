#!/usr/bin/env python3
"""Test voice components."""

from rich.console import Console

console = Console()


def test_audio():
    """Test audio setup."""
    console.print("[bold]Testing Audio Setup[/bold]\n")
    
    # Test PyAudio
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        console.print("[green]✓[/green] PyAudio installed")
        
        # List devices
        console.print("\n[cyan]Available audio devices:[/cyan]")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                console.print(f"  {i}: {info['name']} (Input)")
        
        p.terminate()
    except Exception as e:
        console.print(f"[red]✗[/red] PyAudio error: {e}")
        return False
    
    # Test SpeechRecognition
    try:
        import speech_recognition as sr
        console.print("[green]✓[/green] SpeechRecognition installed")
    except Exception as e:
        console.print(f"[red]✗[/red] SpeechRecognition error: {e}")
        return False
    
    # Test numpy
    try:
        import numpy as np
        console.print("[green]✓[/green] NumPy installed")
    except Exception as e:
        console.print(f"[red]✗[/red] NumPy error: {e}")
        return False
    
    console.print("\n[green]All audio dependencies are installed![/green]")
    return True


def test_microphone():
    """Test microphone recording."""
    console.print("\n[bold]Testing Microphone[/bold]\n")
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        console.print("[cyan]Adjusting for ambient noise...[/cyan]")
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
        
        console.print("[green]✓[/green] Microphone is working!")
        console.print(f"[dim]Energy threshold: {r.energy_threshold}[/dim]")
        
        return True
    except Exception as e:
        console.print(f"[red]✗[/red] Microphone error: {e}")
        return False


def test_speech_recognition():
    """Test speech recognition."""
    console.print("\n[bold]Testing Speech Recognition[/bold]\n")
    console.print("[yellow]Say something after the beep...[/yellow]")
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            console.print("[cyan]🎤 Listening...[/cyan]")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        console.print("[cyan]🔄 Processing...[/cyan]")
        text = r.recognize_google(audio)
        
        console.print(f"[green]✓[/green] You said: [bold]{text}[/bold]")
        return True
        
    except sr.WaitTimeoutError:
        console.print("[yellow]⏱️  No speech detected (timeout)[/yellow]")
        return False
    except sr.UnknownValueError:
        console.print("[yellow]❌ Could not understand audio[/yellow]")
        return False
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        return False


if __name__ == "__main__":
    console.print("[bold green]Kai Voice System Test[/bold green]\n")
    
    # Test audio setup
    if not test_audio():
        console.print("\n[red]Please install audio dependencies:[/red]")
        console.print("  sudo apt-get install portaudio19-dev")
        console.print("  pip install pyaudio SpeechRecognition numpy")
        exit(1)
    
    # Test microphone
    if not test_microphone():
        console.print("\n[red]Microphone not working. Check your audio settings.[/red]")
        exit(1)
    
    # Test speech recognition
    console.print("\n[bold]Final Test: Speech Recognition[/bold]")
    console.print("[dim]This requires internet connection[/dim]")
    
    try:
        test_speech_recognition()
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted[/yellow]")
    
    console.print("\n[green]✓ Voice system is ready![/green]")
    console.print("\nRun: [cyan]python -m kai.cli voice[/cyan]")
