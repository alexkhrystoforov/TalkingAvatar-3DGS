#!/usr/bin/env python3
"""
Baseline Wav2Lip Demo - Safety Net Implementation

This provides a working text-to-video pipeline using Wav2Lip
while we develop the 3DGS solution.

Usage:
    python scripts/baseline_wav2lip.py \
        --video data/raw/training_video.mp4 \
        --text "Hello, this is a test." \
        --output outputs/videos/baseline.mp4
"""

import argparse
import sys
from pathlib import Path
import subprocess
import tempfile

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import OUTPUT_DIR, EXTERNAL_DIR, VIDEOS_DIR


def generate_audio_from_text(text: str, output_path: Path, voice: str = "en-US-AriaNeural"):
    """Generate audio from text using edge-tts (Python 3.12 compatible)"""
    try:
        print(f"🗣️  Generating audio from text: '{text[:50]}...'")
        print(f"   Using voice: {voice}")

        # Use edge-tts (Microsoft Edge TTS, works with Python 3.12)
        cmd = [
            "edge-tts",
            "--text", text,
            "--voice", voice,
            "--write-media", str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Audio generated: {output_path}")
        return True

    except FileNotFoundError:
        print("❌ edge-tts not found. Install with: pip install edge-tts")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ TTS failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        return False


def run_wav2lip(video_path: Path, audio_path: Path, output_path: Path):
    """Run Wav2Lip inference"""

    wav2lip_dir = EXTERNAL_DIR / "Wav2Lip"

    if not wav2lip_dir.exists():
        print(f"❌ Wav2Lip not found at {wav2lip_dir}")
        print("Run setup_runpod.sh first!")
        return False

    # Download Wav2Lip checkpoint if not exists
    checkpoint_path = wav2lip_dir / "checkpoints" / "wav2lip_gan.pth"
    if not checkpoint_path.exists():
        print("📥 Downloading Wav2Lip checkpoint...")
        checkpoint_path.parent.mkdir(exist_ok=True)
        subprocess.run([
            "wget",
            "https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA",
            "-O", str(checkpoint_path)
        ], check=True)

    print(f"🎬 Running Wav2Lip...")
    print(f"   Video: {video_path}")
    print(f"   Audio: {audio_path}")

    try:
        cmd = [
            "python", str(wav2lip_dir / "inference.py"),
            "--checkpoint_path", str(checkpoint_path),
            "--face", str(video_path),
            "--audio", str(audio_path),
            "--outfile", str(output_path),
            "--pads", "0", "10", "0", "0",  # Top, bottom, left, right padding
            "--resize_factor", "1",
        ]

        subprocess.run(cmd, check=True, cwd=wav2lip_dir)
        print(f"✅ Video generated: {output_path}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Wav2Lip failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Baseline Wav2Lip Demo")
    parser.add_argument("--video", type=Path, required=True, help="Input video file")
    parser.add_argument("--audio", type=Path, help="Audio file (if not using TTS)")
    parser.add_argument("--text", type=str, help="Text to synthesize (if not using audio file)")
    parser.add_argument("--voice", type=str, default="en-US-AriaNeural",
                        help="Voice for edge-tts (default: en-US-AriaNeural)")
    parser.add_argument("--output", type=Path, required=True, help="Output video file")

    args = parser.parse_args()

    # Validate inputs
    if not args.video.exists():
        print(f"❌ Video not found: {args.video}")
        return 1

    if not args.audio and not args.text:
        print("❌ Must provide either --audio or --text")
        return 1

    # Create output directory
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # Generate or use audio
    if args.text:
        # Generate audio from text
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio_path = Path(tmp.name)

        success = generate_audio_from_text(
            args.text,
            audio_path,
            args.voice
        )

        if not success:
            return 1
    else:
        audio_path = args.audio
        if not audio_path.exists():
            print(f"❌ Audio not found: {audio_path}")
            return 1

    # Run Wav2Lip
    success = run_wav2lip(args.video, audio_path, args.output)

    # Cleanup temp audio if generated
    if args.text and audio_path.exists():
        audio_path.unlink()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
