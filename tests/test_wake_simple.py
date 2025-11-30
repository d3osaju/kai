#!/usr/bin/env python3
"""Simple wake word test - triggers on any loud sound."""

import pyaudio
import numpy as np
from rich.console import Console

console = Console()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

console.print("[bold green]Simple Wake Word Test[/bold green]")
console.print("This will trigger on any loud sound\n")

# Initialize audio
audio = pyaudio.PyAudio()

# Open stream
console.print("[cyan]Opening microphone...[/cyan]")
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# Calibrate
console.print("[cyan]Calibrating (stay quiet)...[/cyan]")
energies = []
for _ in range(10):
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    energy = np.sqrt(np.mean(audio_data**2))
    if not np.isnan(energy) and energy > 0:
        energies.append(energy)

if energies:
    ambient = np.mean(energies)
else:
    ambient = 100.0  # Default if no valid readings

threshold = max(ambient * 3.0, 300.0)  # Minimum threshold of 300

console.print(f"[green]✓ Calibrated![/green]")
console.print(f"📊 Ambient energy: {ambient:.1f}")
console.print(f"📊 Trigger threshold: {threshold:.1f}\n")
console.print("[yellow]Make a loud sound or say something![/yellow]")
console.print("[dim]Press Ctrl+C to stop[/dim]\n")

try:
    trigger_count = 0
    while True:
        # Read audio
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        energy = np.sqrt(np.mean(audio_data**2))
        
        # Skip invalid readings
        if np.isnan(energy) or energy < 0:
            continue
        
        # Show energy level
        bars = int(min((energy / threshold) * 20, 20))
        bar_display = "█" * bars
        
        # Print energy meter (overwrite same line)
        print(f"\r🔊 Energy: {energy:6.1f} [{bar_display:<20}]", end="", flush=True)
        
        # Trigger on high energy
        if energy > threshold:
            trigger_count += 1
            print(f"\n[{trigger_count}] ✨ TRIGGERED! Energy: {energy:.1f}")
            console.print("[green]This would activate Kai![/green]\n")
            
            # Wait a bit to avoid multiple triggers
            import time
            time.sleep(1)
            
except KeyboardInterrupt:
    print("\n")
    console.print("[yellow]Test stopped[/yellow]")
    console.print(f"Total triggers: {trigger_count}")

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
