# Kai: The Voice of Linux

**Open-Source, Privacy-Focused AI Assistant with Natural Voice Interaction**

Kai is a powerful, locally-running AI assistant designed specifically for Linux users who value privacy, customization, and control. Unlike cloud-based assistants, Kai processes everything on your device with natural voice interaction.

## ✨ Features

- 🎤 **Voice Interaction** - Wake word detection ("Hey Kai"), speech recognition, and natural voice responses
- 💬 **Conversation Mode** - Stay awake for follow-up questions, no need to repeat wake word
- ⚡ **Fast Response** - Parallel sentence processing for near-zero lag between sentences
- ⌨️ **Keyboard Interrupt** - Press SPACE to stop Kai mid-sentence
- 🔊 **Voice Control** - Adjustable speed and volume for comfortable listening
- 🤖 **Local AI** - Powered by Ollama + Llama 3.2 3B, runs entirely on your machine
- 🔒 **Privacy First** - All AI processing happens locally, your data stays yours
- 🐧 **Linux Native** - Deep system integration with D-Bus and desktop environments
- 📦 **Easy Install** - One-command installation or .deb package for Debian/Ubuntu
- 🧩 **Modular Design** - Extend functionality with plugins
- 🆓 **Fully Open Source** - Transparent, auditable, community-driven

## 🚀 Quick Start

### Prerequisites

- Linux (Ubuntu 22.04+, Fedora 38+, Arch, etc.)
- Python 3.11 or higher
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Internet connection (for voice features)
- Microphone and speakers

### Installation

#### Option 1: Debian/Ubuntu Package (Recommended)

```bash
# Download the .deb package
wget https://github.com/yourusername/kai/releases/download/v1.0.0/kai-assistant_1.0.0-1_all.deb

# Install
sudo dpkg -i kai-assistant_1.0.0-1_all.deb
sudo apt-get install -f

# Done! Kai is now available system-wide
kai voice
```

#### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/kai.git
cd kai

# Run the installer (installs everything!)
./install.sh
```

The installer automatically:
- ✅ Installs system dependencies (audio libraries)
- ✅ Installs Ollama and downloads Llama 3.2 3B model
- ✅ Creates Python virtual environment
- ✅ Installs all Python packages
- ✅ Sets up Kai

### First Run

```bash
# Activate virtual environment
source venv/bin/activate

# Test voice (recommended first step)
python tests/test_gtts.py

# Voice demo (continuous listening)
python tests/voice_demo.py

# Full voice mode (with wake word)
python -m kai.cli voice

# Text mode (type your questions)
python -m kai.cli start
```

## 💬 Usage

### Voice Mode (Recommended)

```bash
# Basic usage
kai voice

# With custom settings
kai voice --volume 120 --speed 1.5 --sensitivity 0.3

# Options:
#   --volume, -v      Volume level (0-100, default: 100)
#   --speed           Voice speed (0.5-2.0, default: 1.2)
#   --sensitivity, -s Wake word sensitivity (0.0-1.0, default: 0.3)
```

**How it works:**
1. Say **"Hey Kai"** or **"Kai"** to wake up
2. Kai says "Yes?" and starts listening
3. Ask your question naturally
4. Kai responds with voice
5. **Stay in conversation** - ask follow-up questions without wake word
6. Press **SPACE** to interrupt Kai mid-sentence
7. After 5 seconds of silence, Kai goes back to sleep

**Example conversation:**
```
You: "Hey Kai"
Kai: "Yes?"
You: "How do I check disk space?"
Kai: "To check disk space, just run d-f dash h in your terminal..."
You: "What about memory usage?"  ← No wake word needed!
Kai: "For memory, use the free command with dash h flag..."
[5 seconds of silence]
Kai: "Going to sleep..."
```
You: "Hey Kai"
Kai: 🔊 "Hi! How can I help you?"

You: "What is Linux?"
Kai: 🔊 [Speaks natural answer]

You: "Tell me a joke"
Kai: 🔊 [Tells joke with natural voice]
```

### Voice Demo (No Wake Word)

```bash
python tests/voice_demo.py
```

Listens continuously and responds to everything you say. Great for testing!

### Text Mode

```bash
# Interactive mode
python -m kai.cli start

# Single query
python -m kai.cli query "What is open source?"
```

### Options

```bash
# Adjust wake word sensitivity (0.0-1.0)
python -m kai.cli voice --sensitivity 0.8

# Adjust voice speed (1.0=normal, 1.5=faster, 2.0=very fast)
python -m kai.cli voice --speed 1.5

# Combine options
python -m kai.cli voice --sensitivity 0.8 --speed 1.5

# Disable voice output (text only)
python -m kai.cli voice --no-speak
```

## 🎙️ Voice Features

### Natural Voice Quality

Kai uses **Google Text-to-Speech** for natural, human-like voice responses:
- ✅ Clear and professional
- ✅ Natural rhythm and intonation
- ✅ Easy to understand
- ✅ Supports 100+ languages
- ✅ **Streaming mode** - Long responses start playing immediately (sentence-by-sentence)

### Wake Word Detection

- Responds to "Hey Kai" or "Kai"
- Adjustable sensitivity
- Low latency (~100ms)
- Runs locally

### Speech Recognition

- Google Speech API (free, no key needed)
- Automatic noise adjustment
- High accuracy
- Requires internet

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         User Interface Layer            │
│   Voice Input  │  CLI  │  Text Mode     │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│        Core Processing Layer            │
│  Intent Recognition │ Context Manager   │
│     Plugin Manager  │  Config System    │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         AI/ML Processing Layer          │
│  Speech-to-Text │ LLM │ Text-to-Speech  │
│   (Google API)  │(Ollama)│  (gTTS)      │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Integration Layer               │
│  System Control │ Desktop │ Plugins     │
└─────────────────────────────────────────┘
```

## 🔧 Configuration

Config file: `~/.config/kai/config.yaml`

```yaml
core:
  language: en-US
  wake_word: hey kai

models:
  llm: llama3.2:3b

plugins:
  enabled:
    - system_control
    - general_query
```

## 🧩 Plugin System

Kai uses a modular plugin architecture. Create custom plugins:

```python
from kai.plugins.base import Plugin
from kai.core.intent import Intent

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="my_plugin",
            version="1.0.0",
            intents=["custom_action"]
        )
    
    async def handle_intent(self, intent: Intent):
        # Your custom logic
        return "Action completed!"
```

Built-in plugins:
- **system_control** - Launch/close applications
- **general_query** - AI-powered responses

## 🧪 Testing

```bash
source venv/bin/activate

# Test natural voice
python tests/test_gtts.py

# Test different voice speeds
python tests/test_speed.py

# Test streaming vs non-streaming (for long responses)
python tests/test_streaming.py

# Test microphone
python tests/test_wake_simple.py

# Test speech recognition
python tests/test_voice.py

# Test LLM integration
python tests/demo.py

# Voice demo (full test)
python tests/voice_demo.py
```

## 📊 Performance

On your system (16 cores, 14GB RAM, NVIDIA GPU):
- Wake word detection: ~100ms
- Speech recognition: 1-2 seconds
- LLM response: 1-2 seconds
- Text-to-speech: **~0.5s to first audio** (streaming mode)
- **Total: 3-5 seconds to start hearing response**

**Note**: Long responses use streaming mode - you hear the first sentence while the rest is still being processed!

## 🛠️ System Requirements

### Minimum
- CPU: Dual-core 2.0 GHz
- RAM: 4GB
- Storage: 10GB
- OS: Linux kernel 5.4+

### Recommended
- CPU: Quad-core 3.0 GHz
- RAM: 8GB+
- Storage: 20GB SSD
- GPU: NVIDIA/AMD (optional, for acceleration)

### System Dependencies

Installed automatically by `install.sh`:
```bash
portaudio19-dev    # Audio I/O
python3-pyaudio    # Python audio bindings
mpg123             # Audio playback
alsa-utils         # Audio utilities
```

## 🐛 Troubleshooting

### Wake word not triggering?

```bash
# Test microphone
arecord -d 3 test.wav && aplay test.wav

# Increase sensitivity
python -m kai.cli voice --sensitivity 0.5

# Or use voice demo (no wake word needed)
python tests/voice_demo.py
```

### Wake word triggering on any sound?

```bash
# Decrease sensitivity (default is now 0.3)
python -m kai.cli voice --sensitivity 0.2

# Or calibrate to find the right setting
python tests/test_wake_calibration.py

# Use simple test mode
python tests/test_wake_calibration.py simple
```

### No voice output?

```bash
# Test TTS
python tests/test_gtts.py

# Check internet connection
ping google.com

# Test speakers
speaker-test -t wav -c 2
```

### Speech not recognized?

- Check internet connection (required for Google Speech API)
- Speak clearly and at normal pace
- Reduce background noise
- Test: `python tests/test_voice.py`

### Kai responding to its own voice?

This is an audio feedback issue. Solutions:
- **Best:** Use headphones for audio output
- Position speakers away from microphone
- Lower speaker volume
- The system now waits for audio to finish before listening
- See `docs/AUDIO_FEEDBACK_FIX.md` for details

### High ambient noise?

Your environment has high background noise. Solutions:
- Close windows
- Turn off fans/AC
- Move to quieter room
- Use voice demo instead: `python tests/voice_demo.py`
- Increase sensitivity: `--sensitivity 0.9`

## 📁 Project Structure

```
kai/
├── kai/                    # Main package
│   ├── core/              # Core functionality
│   │   ├── assistant.py   # Main assistant
│   │   ├── config.py      # Configuration
│   │   └── intent.py      # Intent recognition
│   ├── ai/                # AI components
│   │   └── llm.py         # Ollama integration
│   ├── audio/             # Voice features
│   │   ├── stt.py         # Speech-to-text
│   │   ├── tts_gtts.py    # Text-to-speech (natural)
│   │   └── wake_word.py   # Wake word detection
│   ├── plugins/           # Plugin system
│   │   ├── base.py        # Plugin base class
│   │   ├── manager.py     # Plugin manager
│   │   ├── system_control/
│   │   └── general_query/
│   └── cli.py             # CLI interface
├── tests/                 # Test scripts
│   ├── test_gtts.py       # Test TTS
│   ├── test_voice.py      # Test speech recognition
│   ├── test_wake_simple.py # Test microphone
│   ├── demo.py            # LLM demo
│   └── voice_demo.py      # Full voice demo
├── install.sh             # Installation script
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See `CONTRIBUTING.md` for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with amazing open-source projects:
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Llama 3.2](https://ollama.com/library/llama3.2) - Meta's language model
- [gTTS](https://github.com/pndurette/gTTS) - Google Text-to-Speech
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Speech recognition library

## 🚀 Quick Commands Reference

```bash
# Installation
./install.sh

# Activation (always run first!)
source venv/bin/activate

# Voice modes
python tests/voice_demo.py                      # Continuous listening
python -m kai.cli voice                         # With wake word
python -m kai.cli voice --sensitivity 0.8       # Adjust sensitivity
python -m kai.cli voice --speed 1.5             # Faster voice (1.5x)
python -m kai.cli voice --speed 2.0             # Very fast (2x)
python -m kai.cli voice -s 0.8 --speed 1.5      # Combined

# Text mode
python -m kai.cli start                         # Interactive
python -m kai.cli query "question"              # Single query

# Testing
python tests/test_gtts.py                       # Test voice
python tests/test_speed.py                      # Test different speeds
python tests/test_wake_simple.py                # Test microphone
python tests/test_voice.py                      # Test speech recognition
```

## 💡 Tips

1. **Start with voice demo** - Most reliable way to test
2. **Quiet environment** - Better for voice recognition
3. **Speak clearly** - Normal pace, clear pronunciation
4. **Wait for acknowledgment** - Listen for "Hi! How can I help you?"
5. **Adjust sensitivity** - Find what works for your environment

## 🌟 What Makes Kai Special

- **Privacy**: All AI processing happens locally
- **Natural Voice**: Professional-quality speech synthesis
- **Open Source**: Fully transparent and auditable
- **Linux Native**: Built specifically for Linux
- **Extensible**: Plugin system for unlimited functionality
- **No Cloud**: Works without sending data to external servers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/d3osaju/kai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/d3osaju/kai/discussions)

---

**Made with ❤️ by the deo, for the Linux community.**

**Get started:** `./install.sh && source venv/bin/activate && python tests/voice_demo.py`
