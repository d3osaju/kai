#!/usr/bin/env python3
"""Demo script for Kai with Ollama integration."""

import asyncio
from kai.core.assistant import Assistant
from rich.console import Console
from rich.panel import Panel

console = Console()


async def main():
    """Run Kai demo."""
    console.print(Panel.fit(
        "[bold green]Kai AI Assistant Demo[/bold green]\n"
        "Powered by Ollama + Llama 3.2 3B",
        border_style="green"
    ))
    
    console.print("\n[cyan]Initializing Kai...[/cyan]")
    assistant = Assistant()
    await assistant.initialize()
    console.print("[green]✓ Kai is ready![/green]\n")
    
    # Demo queries
    queries = [
        "What is Linux?",
        "Tell me about open source software",
        "What's the difference between Ubuntu and Debian?",
        "How do I list files in a directory?",
    ]
    
    for query in queries:
        console.print(f"\n[bold cyan]You:[/bold cyan] {query}")
        console.print("[dim]Thinking...[/dim]")
        
        response = await assistant.async_query(query)
        
        console.print(f"[bold green]Kai:[/bold green] {response}")
        console.print("[dim]" + "─" * 80 + "[/dim]")
        
        # Small delay for readability
        await asyncio.sleep(1)
    
    console.print("\n[yellow]Demo complete! Try running 'kai start' for interactive mode.[/yellow]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted.[/yellow]")
