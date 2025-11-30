#!/usr/bin/env python3
"""Test text-to-speech."""

from kai.audio.tts import TextToSpeech
from rich.console import Console

console = Console()

console.print("[bold green]Kai Text-to-Speech Test[/bold green]\n")

# Initialize TTS
console.print("[cyan]Initializing TTS engine...[/cyan]")
try:
    tts = TextToSpeech(rate=175, volume=1.0)
    console.print("[green]✓ TTS initialized[/green]\n")
except Exception as e:
    console.print(f"[red]Error:[/red] {e}")
    exit(1)

# List available voices
console.print("[cyan]Available voices:[/cyan]")
tts.list_voices()
console.print()

# Test phrases
test_phrases = [
    "Hello! I am Kai, your AI assistant.",
    "I can help you with questions about Linux and open source.",
    "How can I assist you today?",
]

console.print("[yellow]Testing speech output...[/yellow]\n")

for i, phrase in enumerate(test_phrases, 1):
    console.print(f"[{i}] [cyan]Speaking:[/cyan] {phrase}")
    tts.speak(phrase)
    console.print("[green]✓ Done[/green]\n")

console.print("[green]TTS test complete![/green]")
console.print("\nYou can now use voice mode with:")
console.print("[cyan]python -m kai.cli voice[/cyan]")
