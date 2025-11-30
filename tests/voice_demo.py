#!/usr/bin/env python3
"""Voice demo for Kai - Simple wake word test."""

import asyncio
from kai.core.assistant import Assistant
from kai.audio.stt import SpeechRecognizer
from kai.audio.tts import TextToSpeech
from rich.console import Console

console = Console()


async def main():
    """Run voice demo."""
    console.print("[bold green]Kai Voice Demo with Speech[/bold green]")
    console.print("This demo will listen and respond with voice\n")
    
    # Initialize
    console.print("[cyan]Initializing Kai...[/cyan]")
    assistant = Assistant()
    await assistant.initialize()
    
    console.print("[cyan]Initializing speech recognition...[/cyan]")
    stt = SpeechRecognizer()
    
    console.print("[cyan]Initializing text-to-speech (Google TTS)...[/cyan]")
    try:
        from kai.audio.tts_gtts import GoogleTTS
        tts = GoogleTTS(lang='en', slow=False, speed=1.2)  # 20% faster
        console.print("[green]✓ Natural voice responses enabled (1.2x speed)[/green]")
    except Exception as e:
        console.print(f"[yellow]Warning: TTS failed: {e}[/yellow]")
        tts = None
    
    console.print("\n[green]✓ Ready![/green]")
    console.print("[yellow]Say something after the beep...[/yellow]\n")
    
    try:
        while True:
            # Listen for speech
            console.print("[dim]🎤 Listening... (speak now)[/dim]")
            text = stt.listen(timeout=10)
            
            if text:
                console.print(f"\n[cyan]You said:[/cyan] {text}")
                
                # Check for exit command
                if any(word in text.lower() for word in ["exit", "quit", "goodbye", "stop"]):
                    console.print("[yellow]Goodbye![/yellow]")
                    if tts:
                        tts.speak("Goodbye!")
                    break
                
                # Process with Kai
                console.print("[dim]Thinking...[/dim]")
                response = await assistant.async_query(text)
                console.print(f"[green]Kai:[/green] {response}\n")
                
                # Speak the response
                if tts:
                    console.print("[dim]🔊 Speaking...[/dim]")
                    tts.speak(response)
                    console.print()
            else:
                console.print("[yellow]No speech detected, trying again...[/yellow]\n")
                
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo stopped[/yellow]")
        if tts:
            tts.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
