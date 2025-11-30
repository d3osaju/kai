# Kai Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install
```bash
git clone https://github.com/yourusername/kai.git
cd kai
./install.sh
```

### 2. Activate
```bash
source venv/bin/activate
```

### 3. Run
```bash
python tests/voice_demo.py
```

That's it! Start talking to Kai! 🎤

---

## 📋 Common Commands

### Voice Modes
```bash
# Continuous listening (easiest)
python tests/voice_demo.py

# With wake word "Hey Kai"
python -m kai.cli voice

# Faster voice (1.5x speed)
python -m kai.cli voice --speed 1.5

# More sensitive wake word
python -m kai.cli voice --sensitivity 0.8

# Combined (recommended)
python -m kai.cli voice --sensitivity 0.8 --speed 1.5
```

### Text Mode
```bash
# Interactive chat
python -m kai.cli start

# Single question
python -m kai.cli query "What is Linux?"
```

### Testing
```bash
# Test voice output
python tests/test_gtts.py

# Test different speeds
python tests/test_speed.py

# Test streaming (long responses)
python tests/test_streaming.py

# Test microphone
python tests/test_wake_simple.py
```

---

## 🎯 Quick Tips

1. **Always activate venv first:**
   ```bash
   source venv/bin/activate
   ```

2. **Start with voice demo** (no wake word needed):
   ```bash
   python tests/voice_demo.py
   ```

3. **Adjust for your environment:**
   - Noisy? → `--sensitivity 0.9`
   - Quiet? → `--sensitivity 0.7`
   - Want faster? → `--speed 1.5`

4. **Say "exit" or "quit"** to stop voice mode

5. **Speak clearly** at normal pace

---

## 🔧 Troubleshooting

### Wake word not working?
```bash
# Test microphone
arecord -d 3 test.wav && aplay test.wav

# Use voice demo instead (no wake word)
python tests/voice_demo.py

# Or increase sensitivity
python -m kai.cli voice --sensitivity 0.9
```

### No voice output?
```bash
# Test TTS
python tests/test_gtts.py

# Check internet (required for Google TTS)
ping google.com

# Test speakers
speaker-test -t wav -c 2
```

### Speech not recognized?
- Check internet connection
- Speak clearly and at normal pace
- Reduce background noise
- Test: `python tests/test_voice.py`

---

## 📊 Performance

**Typical interaction:**
- Wake word detection: ~100ms
- Speech recognition: 1-2s
- AI response: 1-2s
- Voice output: **~0.5s to first audio** (streaming!)
- **Total: 3-5s to start hearing response**

**Long responses:** Audio starts playing immediately while the rest is being generated! 🚀

---

## 🎤 Voice Interaction Flow

```
1. Say "Hey Kai"
   ↓
2. Wait for "Hi! How can I help you?"
   ↓
3. Ask your question
   ↓
4. Kai responds with voice
   ↓
5. Repeat or say "exit"
```

---

## 📁 Important Files

- `README.md` - Complete documentation
- `SUMMARY.md` - Project overview
- `CHANGELOG.md` - Recent changes
- `install.sh` - Installation script
- `requirements.txt` - Dependencies

---

## 🆘 Need Help?

1. Check `README.md` for detailed docs
2. Run tests to verify setup
3. Open an issue on GitHub

---

## 🌟 Recommended First Run

```bash
# 1. Install
./install.sh

# 2. Activate
source venv/bin/activate

# 3. Test voice
python tests/test_gtts.py

# 4. Try voice demo
python tests/voice_demo.py

# 5. Use full assistant
python -m kai.cli voice --sensitivity 0.8 --speed 1.5
```

---

**Made with ❤️ for Linux users**

For complete documentation, see **README.md**
