"""Test and calibrate wake word detection sensitivity."""

from kai.audio.wake_word import WakeWordDetector
import time

def test_calibration():
    """Test wake word detection with visual feedback."""
    
    print("\n" + "=" * 70)
    print("🎤 WAKE WORD CALIBRATION TEST")
    print("=" * 70)
    print("\nThis will help you find the right sensitivity setting.")
    print("\nInstructions:")
    print("1. The detector will calibrate for ambient noise")
    print("2. Try making different sounds:")
    print("   - Normal talking")
    print("   - Loud talking")
    print("   - Clapping")
    print("   - Keyboard typing")
    print("   - Background noise")
    print("3. Watch which sounds trigger detection")
    print("4. Adjust sensitivity if needed")
    print("\n💡 Goal: Only trigger on intentional speech, not random sounds")
    print("\nPress Ctrl+C to stop\n")
    
    # Test different sensitivity levels
    sensitivities = [0.3, 0.5, 0.7]
    
    for sens in sensitivities:
        print("\n" + "=" * 70)
        print(f"Testing with sensitivity: {sens}")
        print("=" * 70)
        
        detector = WakeWordDetector(sensitivity=sens)
        
        trigger_count = [0]
        
        def on_trigger():
            trigger_count[0] += 1
            print(f"🎯 TRIGGER #{trigger_count[0]} - Wake word detected!")
        
        detector.start(on_trigger)
        
        print(f"\n⏱️  Testing for 15 seconds...")
        print("Try making sounds and see what triggers detection:\n")
        
        try:
            time.sleep(15)
        except KeyboardInterrupt:
            print("\n\n⏹️  Test stopped by user")
            detector.stop()
            break
        
        detector.stop()
        
        print(f"\n📊 Results for sensitivity {sens}:")
        print(f"   Total triggers: {trigger_count[0]}")
        
        if trigger_count[0] == 0:
            print("   ⚠️  Too strict - might miss real wake words")
        elif trigger_count[0] <= 3:
            print("   ✅ Good - only triggered on intentional sounds")
        elif trigger_count[0] <= 6:
            print("   ⚠️  Moderate - some false positives")
        else:
            print("   ❌ Too sensitive - many false positives")
        
        if sens != sensitivities[-1]:
            print("\nMoving to next sensitivity level in 3 seconds...")
            time.sleep(3)
    
    print("\n" + "=" * 70)
    print("📋 RECOMMENDATIONS:")
    print("=" * 70)
    print("\nBased on your environment:")
    print("• Quiet room: Use --sensitivity 0.5")
    print("• Normal room: Use --sensitivity 0.3 (default)")
    print("• Noisy room: Use --sensitivity 0.2")
    print("\nTo use:")
    print("  python -m kai.cli voice --sensitivity 0.3")
    print("\n" + "=" * 70 + "\n")

def test_simple():
    """Simple continuous test with one sensitivity."""
    
    print("\n" + "=" * 70)
    print("🎤 SIMPLE WAKE WORD TEST")
    print("=" * 70)
    
    sensitivity = float(input("\nEnter sensitivity (0.1-0.9, default 0.3): ") or "0.3")
    
    print(f"\nTesting with sensitivity: {sensitivity}")
    print("Make sounds and watch for triggers...")
    print("Press Ctrl+C to stop\n")
    
    detector = WakeWordDetector(sensitivity=sensitivity)
    
    trigger_count = [0]
    
    def on_trigger():
        trigger_count[0] += 1
        print(f"\n🎯 TRIGGER #{trigger_count[0]} at {time.strftime('%H:%M:%S')}")
    
    detector.start(on_trigger)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Test stopped")
        print(f"📊 Total triggers: {trigger_count[0]}")
    
    detector.stop()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'simple':
        test_simple()
    else:
        test_calibration()
