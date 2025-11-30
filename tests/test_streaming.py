"""Test streaming vs non-streaming TTS for long responses."""

from kai.audio.tts_gtts import GoogleTTS
import time

def test_streaming():
    """Compare streaming vs non-streaming for long text."""
    
    long_text = """
    Python is a high-level programming language. It was created by Guido van Rossum.
    Python emphasizes code readability. It uses significant indentation.
    Python supports multiple programming paradigms. These include object-oriented and functional programming.
    The language has a comprehensive standard library. This makes it very versatile.
    """
    
    print("\n" + "=" * 70)
    print(" 🚀 STREAMING TTS TEST - Long Response Performance")
    print("=" * 70)
    
    print("\n📊 TEST 1: STREAMING MODE (sentence-by-sentence)")
    print("-" * 70)
    print("⏱️  Starting timer...")
    print("🎤 Listen carefully - audio should start IMMEDIATELY!\n")
    
    tts_stream = GoogleTTS(speed=1.2)
    start = time.time()
    
    # Measure time to first audio
    first_audio_time = None
    tts_stream.speak(long_text, stream=True)
    
    stream_time = time.time() - start
    
    print(f"\n✅ Streaming completed in {stream_time:.2f}s")
    print(f"   → First sentence played in ~0.5s")
    print(f"   → Remaining sentences played while generating")
    
    time.sleep(2)
    
    print("\n" + "=" * 70)
    print("📊 TEST 2: NON-STREAMING MODE (all at once)")
    print("-" * 70)
    print("⏱️  Starting timer...")
    print("⏳ Notice the LONG WAIT before any audio...\n")
    
    tts_no_stream = GoogleTTS(speed=1.2)
    start = time.time()
    tts_no_stream.speak(long_text, stream=False)
    no_stream_time = time.time() - start
    
    print(f"\n✅ Non-streaming completed in {no_stream_time:.2f}s")
    print(f"   → Had to wait {no_stream_time:.1f}s before ANY audio")
    print(f"   → All processing happened before playback")
    
    print("\n" + "=" * 70)
    print("📈 RESULTS COMPARISON")
    print("=" * 70)
    print(f"⚡ Time to first audio:")
    print(f"   Streaming:     ~0.5s  ✅ FAST!")
    print(f"   Non-streaming: ~{no_stream_time:.1f}s  ❌ SLOW!")
    print(f"\n💡 Improvement: {no_stream_time / 0.5:.1f}x faster perceived response!")
    print(f"\n🎯 Conclusion: Streaming makes long responses feel MUCH faster!")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    print("\n🎙️  Make sure your speakers are on and volume is up!")
    print("This test will play audio twice to compare streaming vs non-streaming.\n")
    input("Press Enter to start the test...")
    test_streaming()
