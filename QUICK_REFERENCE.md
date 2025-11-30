# Kai Quick Reference

## Installation

### Debian/Ubuntu
```bash
sudo dpkg -i kai-assistant_1.0.0-1_all.deb
sudo apt-get install -f
```

### From Source
```bash
./install.sh
source venv/bin/activate
```

## Commands

### Voice Mode
```bash
kai voice                              # Start voice assistant
kai voice --volume 120                 # Louder volume
kai voice --speed 1.5                  # Faster speech
kai voice --sensitivity 0.3            # Adjust wake word sensitivity
```

### Text Mode
```bash
kai start                              # Interactive text mode
kai query "your question"              # Single query
```

### Other
```bash
kai --help                             # Show help
kai --version                          # Show version
```

## Voice Interaction

### Wake Word
- Say: **"Hey Kai"** or **"Kai"**
- Kai responds: "Yes?"
- Now you can talk

### Conversation Mode
- After wake word, Kai stays awake
- Ask follow-up questions without repeating wake word
- Goes to sleep after 5 seconds of silence

### Interrupting
- Press **SPACE** while Kai is speaking
- Kai stops immediately
- You can continue talking

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| SPACE | Interrupt Kai while speaking |
| Ctrl+C | Exit voice mode |

## Voice Settings

### Volume
```bash
kai voice --volume 50    # Quiet
kai voice --volume 100   # Normal (default)
kai voice --volume 150   # Loud
```

### Speed
```bash
kai voice --speed 0.8    # Slower
kai voice --speed 1.2    # Normal (default)
kai voice --speed 1.8    # Faster
```

### Sensitivity
```bash
kai voice --sensitivity 0.2    # Less sensitive (fewer false triggers)
kai voice --sensitivity 0.3    # Normal (default)
kai voice --sensitivity 0.5    # More sensitive (easier to trigger)
```

## Example Conversations

### System Information
```
You: "Hey Kai"
Kai: "Yes?"
You: "How do I check disk space?"
Kai: "To check disk space, just run d-f dash h..."
You: "What about memory?"
Kai: "For memory, use the free command..."
```

### File Operations
```
You: "Hey Kai"
Kai: "Yes?"
You: "How do I find large files?"
Kai: "You can use the find command with size parameter..."
```

### Package Management
```
You: "Hey Kai"
Kai: "Yes?"
You: "How do I update my system?"
Kai: "Open a terminal and run sudo apt update..."
```

## Troubleshooting

### No Audio Output
```bash
# Check volume
amixer sget Master

# Test audio
speaker-test -t wav -c 2

# List audio devices
aplay -l
```

### Wake Word Not Working
```bash
# Adjust sensitivity (lower = less sensitive)
kai voice --sensitivity 0.2

# Test microphone
arecord -d 3 test.wav && aplay test.wav
```

### LLM Not Responding
```bash
# Check Ollama
ollama list

# Start Ollama
sudo systemctl start ollama

# Pull model
ollama pull llama3.2:3b
```

## Configuration

### Config Location
- System: `/opt/kai-assistant/`
- User: `~/.config/kai/`

### Audio Devices
Check available devices:
```bash
aplay -l
```

## Development

### Run from Source
```bash
source venv/bin/activate
python -m kai.cli voice
```

### Build Package
```bash
./build-deb.sh
```

### Run Tests
```bash
python tests/test_gtts.py
python tests/test_streaming.py
```

## Tips & Tricks

1. **Speak clearly** - Enunciate words for better recognition
2. **Adjust volume** - Start with `--volume 120` if too quiet
3. **Speed up responses** - Use `--speed 1.5` for faster speech
4. **Reduce false triggers** - Lower sensitivity with `--sensitivity 0.2`
5. **Use conversation mode** - No need to repeat wake word
6. **Interrupt anytime** - Press SPACE to stop Kai

## Common Use Cases

### Quick System Check
```bash
kai query "show me system info"
```

### Voice Assistant
```bash
kai voice --volume 120 --speed 1.3
```

### Quiet Environment
```bash
kai voice --volume 80 --sensitivity 0.4
```

### Fast Responses
```bash
kai voice --speed 1.8
```

## Resources

- Full Documentation: `README.md`
- Development Guide: `DEVELOPMENT.md`
- Changelog: `CHANGELOG.md`
- Debian Package: `README-DEB.md`

## Getting Help

1. Check documentation
2. Run with debug output
3. Check system logs
4. Open an issue on GitHub

---

**Version:** 1.0.0  
**Last Updated:** December 1, 2025
