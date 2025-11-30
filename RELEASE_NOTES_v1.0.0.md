# Kai v1.0.0 Release Notes

**Release Date:** December 1, 2025

## 🎉 Major Release: Production-Ready Voice Assistant

Kai v1.0.0 is the first production-ready release, featuring a complete Debian package, voice-optimized responses, and a smooth conversation experience.

## 🚀 What's New

### Debian Package Distribution
- Complete `.deb` package for easy installation
- One-command install on Debian/Ubuntu systems
- Automatic dependency management
- System-wide `kai` command
- Isolated Python environment (no conflicts)

### Voice-Optimized Responses
- LLM prompts specifically designed for speech
- No more markdown symbols in voice output
- Short, conversational responses (2-3 sentences)
- Natural speech patterns instead of bullet points
- Automatic text cleanup for TTS

### Conversation Mode
- Stay awake after wake word for follow-up questions
- No need to repeat "Hey Kai" during conversation
- Auto-sleep after 5 seconds of silence
- Visual feedback for conversation state

### Keyboard Interrupt
- Press SPACE to interrupt Kai while speaking
- Stops entire response, not just current sentence
- Prevents self-triggering from speaker feedback
- Immediate return to listening mode

### Performance Improvements
- Parallel sentence processing (generate next while playing current)
- Near-zero lag between sentences
- Faster perceived response time
- Efficient audio streaming

### Smart Silence Detection
- Distinguishes between true silence and unclear audio
- Asks you to repeat if it didn't understand
- Only goes to sleep after actual silence
- Better conversation flow

### Volume Control
- `--volume` option to adjust system volume
- Range: 0-100+ (can go above 100 for boost)
- Adjustable voice speed (0.5x - 2.0x)
- Audio device selection support

## 📦 Installation

### Debian/Ubuntu
```bash
sudo dpkg -i kai-assistant_1.0.0-1_all.deb
sudo apt-get install -f
```

### From Source
```bash
git clone <repo-url>
cd kai
./install.sh
```

## 🎯 Usage

### Basic Voice Mode
```bash
kai voice
```

### With Custom Settings
```bash
kai voice --volume 120 --speed 1.5 --sensitivity 0.3
```

### Text Mode
```bash
kai start
```

## 🔧 Technical Details

### Dependencies
- Python 3.11+
- Ollama + Llama 3.2 3B
- mpg123, sox (audio)
- portaudio19-dev, python3-pyaudio
- SpeechRecognition, gTTS, rich, click

### Architecture
- Virtual environment at `/opt/kai-assistant/venv`
- System-wide command wrapper at `/usr/bin/kai`
- Configuration at `~/.config/kai/`
- Modular plugin system

### Performance
- First audio: ~0.5 seconds (16x faster than v0.9.0)
- Sentence streaming with parallel processing
- Efficient memory usage
- Low CPU overhead

## 🐛 Bug Fixes

- Fixed TTS streaming interrupt handling
- Resolved audio device detection issues
- Fixed package conflicts with system Python packages
- Corrected silence detection logic
- Improved error handling and recovery

## 📚 Documentation

New documentation files:
- `DEVELOPMENT.md` - Complete development guide
- `QUICK_REFERENCE.md` - Quick reference card
- `README-DEB.md` - Debian package documentation
- Updated `CHANGELOG.md` with full history
- Updated `README.md` with new features

## 🔄 Upgrade from v0.9.0

If you installed from source:
```bash
cd kai
git pull
./install.sh
```

If you used the old version, uninstall first:
```bash
# Remove old installation
rm -rf venv
pip uninstall kai-assistant

# Install new package
sudo dpkg -i kai-assistant_1.0.0-1_all.deb
```

## ⚠️ Breaking Changes

- `stt.listen()` now returns tuple `(text, status)` instead of just `text`
- Virtual environment location changed to `/opt/kai-assistant/venv`
- Configuration structure updated

## 🎓 Examples

### Example 1: Quick System Check
```bash
kai query "how do I check disk space"
```

### Example 2: Voice Conversation
```bash
kai voice --volume 120

# Say: "Hey Kai"
# Kai: "Yes?"
# You: "How do I update my system?"
# Kai: [responds with voice]
# You: "What about installing packages?"
# Kai: [responds without needing wake word]
```

### Example 3: Fast Voice Mode
```bash
kai voice --speed 1.8 --volume 100
```

## 🙏 Acknowledgments

Thanks to all contributors and testers who helped make this release possible!

## 📝 Known Issues

- Wake word detection may have false positives in noisy environments
  - Workaround: Use `--sensitivity 0.2` for less sensitive detection
- Audio output may be quiet on some systems
  - Workaround: Use `--volume 150` to boost volume
- First response may be slower (LLM warmup)
  - This is normal and improves after first query

## 🔮 What's Next (v1.1.0)

Planned features for next release:
- Offline speech recognition option
- Custom wake word training
- Multi-language support
- Voice customization (pitch, gender)
- Desktop notification integration
- System control plugins (volume, brightness, etc.)
- Calendar and reminder plugins

## 📞 Support

- Documentation: See `README.md` and `DEVELOPMENT.md`
- Issues: Open an issue on GitHub
- Discussions: Join our community discussions

## 📄 License

MIT License - See LICENSE file for details

---

**Enjoy your AI assistant!** 🚀

For detailed changes, see `CHANGELOG.md`
