#!/usr/bin/env python3
"""Test Google TTS (natural voice)."""

from kai.audio.tts_gtts import GoogleTTS
from rich.console import Console
import time

console = Console()

console.print("[bold green]Google TTS Test (Natural Voice)[/bold green]\n")

# Initialize TTS
console.print("[cyan]Initializing Google TTS...[/cyan]")
try:
    tts = GoogleTTS(lang='en', slow=False)
    console.print("[green]✓ Google TTS initialized[/green]\n")
except Exception as e:
    console.print(f"[red]Error:[/red] {e}")
    exit(1)

# Test phrases
test_phrases = [
    "Hello! I am Kai, your AI assistant.",
    "I can help you with questions about Linux and open source.",
    "This voice sounds much more natural than the robotic one!",
]

console.print("[yellow]Testing natural speech output...[/yellow]\n")
console.print("[dim]Note: This requires internet connection[/dim]\n")

for i, phrase in enumerate(test_phrases, 1):
    console.print(f"[{i}] [cyan]Speaking:[/cyan] {phrase}")
    console.print("[dim]🔊 Generating and playing...[/dim]")
    
    start = time.time()
    tts.speak(phrase)
    elapsed = time.time() - start
    
    console.print(f"[green]✓ Done[/green] (took {elapsed:.1f}s)\n")

console.print("[green]Google TTS test complete![/green]")
console.print("\n[yellow]Much better quality, right?[/yellow]")
console.print("\nYou can now use voice mode with natural voice:")
console.print("[cyan]python -m kai.cli voice[/cyan]")

# Cleanup
tts.cleanup()
