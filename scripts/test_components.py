#!/usr/bin/env python3
"""
Test all major components to verify installation
Run this on RunPod after setup to ensure everything works
"""

import sys
import torch

def test_pytorch():
    """Test PyTorch and CUDA"""
    print("\n" + "="*60)
    print("🔥 Testing PyTorch and CUDA")
    print("="*60)

    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")

    if not torch.cuda.is_available():
        print("❌ CUDA not available! This project requires GPU.")
        return False

    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    mem = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"GPU Memory: {mem:.2f} GB")

    # Test basic tensor operations
    x = torch.randn(1000, 1000, device='cuda')
    y = torch.matmul(x, x)
    print(f"✅ CUDA tensor operations working")

    return True

def test_gaussian_rasterization():
    """Test diff-gaussian-rasterization"""
    print("\n" + "="*60)
    print("🎨 Testing Gaussian Rasterization")
    print("="*60)

    try:
        from diff_gaussian_rasterization import GaussianRasterizationSettings, GaussianRasterizer
        print("✅ diff-gaussian-rasterization imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import diff-gaussian-rasterization: {e}")
        print("   This is critical for 3DGS rendering")
        return False

def test_audio():
    """Test audio processing libraries"""
    print("\n" + "="*60)
    print("🎵 Testing Audio Processing")
    print("="*60)

    try:
        import librosa
        import soundfile as sf
        import torchaudio
        print(f"✅ librosa version: {librosa.__version__}")
        print(f"✅ torchaudio version: {torchaudio.__version__}")

        # Test basic audio operations
        import numpy as np
        sample_rate = 16000
        duration = 1.0
        dummy_audio = np.sin(2 * np.pi * 440 * np.linspace(0, duration, int(sample_rate * duration)))
        print(f"✅ Audio tensor created: shape {dummy_audio.shape}")

        return True
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False

def test_tts():
    """Test TTS engine"""
    print("\n" + "="*60)
    print("🗣️  Testing TTS Engine")
    print("="*60)

    try:
        from TTS.api import TTS
        print("✅ TTS imported successfully")

        # List available models
        print("\nAvailable TTS models (first 5):")
        models = TTS.list_models()[:5]
        for model in models:
            print(f"  - {model}")

        return True
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_cv():
    """Test computer vision libraries"""
    print("\n" + "="*60)
    print("👁️  Testing Computer Vision")
    print("="*60)

    try:
        import cv2
        import mediapipe as mp
        from PIL import Image

        print(f"✅ OpenCV version: {cv2.__version__}")
        print(f"✅ MediaPipe version: {mp.__version__}")
        print(f"✅ PIL version: {Image.__version__}")

        # Test basic operations
        import numpy as np
        dummy_img = np.zeros((512, 512, 3), dtype=np.uint8)
        print(f"✅ Test image created: shape {dummy_img.shape}")

        return True
    except Exception as e:
        print(f"❌ CV test failed: {e}")
        return False

def test_gradio():
    """Test Gradio interface"""
    print("\n" + "="*60)
    print("🌐 Testing Gradio")
    print("="*60)

    try:
        import gradio as gr
        print(f"✅ Gradio version: {gr.__version__}")
        return True
    except Exception as e:
        print(f"❌ Gradio test failed: {e}")
        return False

def test_3d_libs():
    """Test 3D processing libraries"""
    print("\n" + "="*60)
    print("🎲 Testing 3D Libraries")
    print("="*60)

    try:
        import pytorch3d
        print(f"✅ PyTorch3D imported successfully")

        import trimesh
        print(f"✅ Trimesh version: {trimesh.__version__}")

        from plyfile import PlyData
        print(f"✅ plyfile imported successfully")

        return True
    except Exception as e:
        print(f"❌ 3D libraries test failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 TESTING TALKINGAVATAR-3DGS COMPONENTS")
    print("="*60)

    results = {
        "PyTorch & CUDA": test_pytorch(),
        "Gaussian Rasterization": test_gaussian_rasterization(),
        "Audio Processing": test_audio(),
        "TTS Engine": test_tts(),
        "Computer Vision": test_cv(),
        "Gradio Interface": test_gradio(),
        "3D Libraries": test_3d_libs(),
    }

    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    for component, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {component}")

    all_passed = all(results.values())

    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Ready to start development.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("Critical: PyTorch/CUDA and Gaussian Rasterization must work.")
    print("="*60 + "\n")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
