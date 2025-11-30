#!/usr/bin/env python3
"""Test different voice speeds."""

from kai.audio.tts_gtts import GoogleTTS
from rich.console import Console

console = Console()

console.print("[bold green]Voice Speed Test[/bold green]\n")

test_text = "Hello! I am Kai, your AI assistant for Linux."

speeds = [
    (1.0, "Normal speed"),
    (1.2, "20% faster (default)"),
    (1.5, "50% faster"),
    (2.0, "Double speed"),
]

console.print("[yellow]Testing different voice speeds...[/yellow]\n")

for speed, description in speeds:
    console.print(f"[cyan]{description} ({speed}x):[/cyan]")
    console.print(f"[dim]Text: {test_text}[/dim]")
    
    tts = GoogleTTS(lang='en', slow=False, speed=speed)
    tts.speak(test_text)
    
    console.print("[green]✓ Done[/green]\n")
    tts.cleanup()

console.print("[green]Speed test complete![/green]")
console.print("\n[yellow]Which speed did you prefer?[/yellow]")
console.print("\nSet your preferred speed:")
console.print("[cyan]python -m kai.cli voice --speed 1.2[/cyan]  # 20% faster")
console.print("[cyan]python -m kai.cli voice --speed 1.5[/cyan]  # 50% faster")
