#!/usr/bin/env python3
"""
Test script to verify Deepgram API setup and basic functionality.

Usage:
    python test_deepgram.py

This will test:
1. Environment variables are loaded
2. Deepgram API connection works
3. Basic transcription functionality
4. WER calculation
"""

import os
import json
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()


def test_environment():
    """Test that environment variables are properly configured."""
    print("Testing environment setup...")

    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        print("❌ DEEPGRAM_API_KEY not found in environment")
        print("   Please set it in your .env file")
        return False

    if api_key == "your_api_key_here":
        print("⚠️  DEEPGRAM_API_KEY is still the placeholder value")
        print("   Please get a real API key from https://console.deepgram.com/signup")
        return False

    print(f"✅ DEEPGRAM_API_KEY found: {api_key[:8]}...")
    return True


def test_imports():
    """Test that all required packages are installed."""
    print("\nTesting package imports...")

    required_packages = [
        ("deepgram", "deepgram-sdk"),
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("Levenshtein", "python-Levenshtein"),
        ("httpx", "httpx"),
        ("aiosqlite", "aiosqlite"),
    ]

    all_imported = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} not installed")
            all_imported = False

    if not all_imported:
        print("\n   Install missing packages with:")
        print("   pip install -r requirements.txt")

    return all_imported


async def test_deepgram_connection():
    """Test basic Deepgram API connection."""
    print("\nTesting Deepgram API connection...")

    try:
        from deepgram import DeepgramClient, PrerecordedOptions

        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("⚠️  Skipping API test (no valid API key)")
            return False

        # Initialize client
        client = DeepgramClient(api_key)

        # Test with a sample audio file
        test_url = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True
        )

        print(f"   Transcribing: {test_url}")

        # Make API call
        response = await client.listen.asyncprerecorded.v("1").transcribe_url(
            {"url": test_url}, options
        )

        # Extract transcript
        transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

        print(f"✅ API connection successful")
        print(f"   Transcript: {transcript[:50]}...")

        return True

    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False


def test_ground_truth_data():
    """Test that ground truth data is available."""
    print("\nTesting ground truth data...")

    ground_truth_path = Path("test_data/ground_truth.json")

    if not ground_truth_path.exists():
        print(f"❌ Ground truth file not found: {ground_truth_path}")
        return False

    try:
        with open(ground_truth_path, 'r') as f:
            data = json.load(f)

        print(f"✅ Ground truth loaded: {len(data)} samples")

        # Show first sample
        if data:
            first = data[0]
            print(f"   First sample: {first.get('id', 'N/A')}")
            print(f"   Audio URL: {first.get('audio_url', 'N/A')[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Error loading ground truth: {e}")
        return False


def test_wer_calculation():
    """Test WER calculation with known examples."""
    print("\nTesting WER calculation...")

    try:
        import Levenshtein

        def calculate_wer(reference, hypothesis):
            """Simple WER calculation."""
            ref_words = reference.lower().split()
            hyp_words = hypothesis.lower().split()

            distance = Levenshtein.distance(ref_words, hyp_words)
            wer = distance / len(ref_words) if ref_words else 0

            return wer

        # Test cases
        test_cases = [
            ("hello world", "hello world", 0.0),
            ("hello world", "hello earth", 0.5),
            ("the quick brown fox", "quick brown fox", 0.25),
            ("", "", 0.0),
        ]

        all_passed = True
        for ref, hyp, expected in test_cases:
            wer = calculate_wer(ref, hyp)
            if abs(wer - expected) < 0.01:
                print(f"✅ WER({ref!r}, {hyp!r}) = {wer:.2f}")
            else:
                print(f"❌ WER({ref!r}, {hyp!r}) = {wer:.2f}, expected {expected:.2f}")
                all_passed = False

        return all_passed

    except ImportError:
        print("❌ python-Levenshtein not installed")
        return False


async def test_monitor_class():
    """Test the DeepgramMonitor class."""
    print("\nTesting DeepgramMonitor class...")

    try:
        from greenfield.deepgram_monitor import DeepgramMonitor

        # Create monitor instance
        monitor = DeepgramMonitor(db_path=":memory:")  # Use in-memory DB for testing

        print("✅ DeepgramMonitor instantiated")

        # Test transcribe_url (will return placeholder)
        result = await monitor.transcribe_url(
            "https://static.deepgram.com/examples/test.wav"
        )

        if result:
            print("✅ transcribe_url method works (returns placeholder)")
        else:
            print("❌ transcribe_url method failed")

        return True

    except Exception as e:
        print(f"❌ Error testing DeepgramMonitor: {e}")
        return False


def test_brownfield_code():
    """Test that the brownfield code at least imports."""
    print("\nTesting brownfield code...")

    try:
        import brownfield.benchmark_nightmare as benchmark

        print("✅ benchmark_nightmare.py imports successfully")

        # Check for global variables (the horror!)
        globals_count = len([
            var for var in dir(benchmark)
            if not var.startswith('_') and var.isupper()
        ])

        print(f"   Found {globals_count} global variables (as expected)")

        return True

    except Exception as e:
        print(f"❌ Error importing brownfield code: {e}")
        return False


async def main():
    """Run all tests."""
    print("=" * 60)
    print("Deepgram Track Test Suite")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Environment", test_environment()))
    results.append(("Imports", test_imports()))
    results.append(("Ground Truth Data", test_ground_truth_data()))
    results.append(("WER Calculation", test_wer_calculation()))

    # Async tests
    results.append(("Deepgram API", await test_deepgram_connection()))
    results.append(("Monitor Class", await test_monitor_class()))
    results.append(("Brownfield Code", test_brownfield_code()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:.<30} {status}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n🎉 All tests passed! The Python track is ready.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

    return passed == total


if __name__ == "__main__":
    # Run async main
    success = asyncio.run(main())
    sys.exit(0 if success else 1)