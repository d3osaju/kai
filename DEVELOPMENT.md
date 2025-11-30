# Kai Development Guide

This guide is for developers who want to contribute to Kai or modify it for their needs.

## Quick Setup for Development

```bash
# Clone the repository
git clone <your-repo-url>
cd kai

# Run the installation script
chmod +x install.sh
./install.sh

# Activate the virtual environment
source venv/bin/activate
```

## Development Workflow

### 1. Making Changes

The project structure:
```
kai/
├── kai/
│   ├── ai/              # LLM integration
│   ├── audio/           # Speech recognition and TTS
│   ├── core/            # Core assistant logic
│   ├── plugins/         # Plugin system
│   └── cli.py           # Command-line interface
├── tests/               # Test files
├── debian/              # Debian packaging
└── requirements.txt     # Python dependencies
```

### 2. Testing Your Changes

```bash
# Activate venv if not already active
source venv/bin/activate

# Test voice mode
python -m kai.cli voice

# Test text mode
python -m kai.cli start

# Run specific tests
python tests/test_gtts.py
python tests/test_streaming.py
```

### 3. Building the Debian Package

```bash
# Install build dependencies
sudo apt-get install debhelper dh-python python3-all python3-setuptools

# Build the package
./build-deb.sh

# Package will be created at: ../kai-assistant_1.0.0-1_all.deb
```

### 4. Testing the Package

```bash
# Install the package
sudo dpkg -i ../kai-assistant_1.0.0-1_all.deb
sudo apt-get install -f

# Test the installed version
kai voice
kai start

# Uninstall when done testing
sudo apt-get remove kai-assistant
```

## Key Components

### Voice Assistant (`kai/cli.py`)

The main voice mode with:
- Wake word detection
- Conversation mode (stays awake)
- Keyboard interrupt (SPACE to stop)
- Volume control

### Text-to-Speech (`kai/audio/tts_gtts.py`)

Features:
- Parallel sentence processing (generate next while playing current)
- Speed adjustment
- Audio device selection
- Interrupt handling

### Speech Recognition (`kai/audio/stt.py`)

Returns status codes:
- `'success'` - Understood speech
- `'timeout'` - No speech detected
- `'unclear'` - Heard but couldn't understand
- `'error'` - Technical error

### LLM Integration (`kai/ai/llm.py`)

Voice-optimized prompts that:
- Keep responses short (2-3 sentences)
- Avoid markdown formatting
- Use natural speech patterns

## Modifying Voice Responses

### Change the System Prompt

Edit `kai/plugins/general_query/plugin.py`:

```python
system_prompt = """Your custom prompt here..."""
```

### Adjust Voice Settings

Edit `kai/audio/tts_gtts.py`:

```python
# Default speed
self.speed = 1.2  # Change this

# Audio device
self.audio_device = 'default'  # Or 'hw:0,3', etc.
```

### Modify Conversation Timeout

Edit `kai/cli.py`:

```python
# Timeout before going to sleep
text, status = stt.listen(timeout=5, recalibrate=False)  # Change timeout here
```

## Adding New Features

### 1. Create a New Plugin

```bash
mkdir kai/plugins/my_plugin
touch kai/plugins/my_plugin/__init__.py
touch kai/plugins/my_plugin/plugin.py
```

Example plugin:
```python
from kai.plugins.base import Plugin
from kai.core.intent import Intent

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(
            name="my_plugin",
            version="1.0.0",
            intents=["my_intent"]
        )
    
    async def handle_intent(self, intent: Intent) -> str:
        return "Hello from my plugin!"
```

### 2. Register the Plugin

Edit `kai/plugins/my_plugin/__init__.py`:
```python
from kai.plugins.my_plugin.plugin import MyPlugin
plugin = MyPlugin()
```

## Version Management

When releasing a new version:

1. Update version in all files:
   - `setup.py`
   - `kai/__init__.py`
   - `kai/cli.py`
   - `debian/changelog`
   - `build-deb.sh`
   - `README-DEB.md`

2. Update `CHANGELOG.md` with changes

3. Build and test the package

## Debugging

### Enable Debug Output

The TTS already has debug output. To add more:

```python
print(f"[DEBUG] Your debug message here")
```

### Check Audio Devices

```bash
# List audio devices
aplay -l

# Test audio output
mpg123 /path/to/test.mp3

# Check volume
amixer sget Master
```

### Test LLM Connection

```bash
# Check if Ollama is running
ollama list

# Test model
ollama run llama3.2:3b "Hello"
```

## Common Issues

### Audio Not Working

```bash
# Install audio dependencies
sudo apt-get install mpg123 sox portaudio19-dev python3-pyaudio

# Test audio device
speaker-test -t wav -c 2
```

### LLM Not Responding

```bash
# Start Ollama service
sudo systemctl start ollama

# Pull model if missing
ollama pull llama3.2:3b
```

### Package Build Fails

```bash
# Clean previous builds
rm -rf build dist *.egg-info debian/kai-assistant

# Install build dependencies
sudo apt-get install debhelper dh-python python3-all python3-setuptools

# Try again
./build-deb.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Update documentation
6. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Comment complex logic

## Testing Checklist

Before submitting changes:

- [ ] Voice mode works (`kai voice`)
- [ ] Text mode works (`kai start`)
- [ ] Wake word detection works
- [ ] Conversation mode works (stays awake)
- [ ] Interrupt works (SPACE key)
- [ ] Audio output is clear
- [ ] No markdown in speech
- [ ] Package builds successfully
- [ ] Package installs and runs

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [SpeechRecognition Library](https://github.com/Uberi/speech_recognition)
- [gTTS Documentation](https://gtts.readthedocs.io/)
- [Debian Packaging Guide](https://www.debian.org/doc/manuals/maint-guide/)

## Getting Help

- Check existing issues
- Read the documentation
- Test with debug output enabled
- Ask in discussions

Happy coding! 🚀
