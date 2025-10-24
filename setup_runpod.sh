#!/bin/bash
set -e

echo "🚀 Setting up TalkingAvatar-3DGS on RunPod..."

# Update system
echo "📦 Updating system packages..."
apt-get update
apt-get install -y git wget curl ffmpeg colmap

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip

# Core dependencies
 pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118
# 3D and rendering
# pip install pytorch3d
pip install ninja  # Required for building extensions
pip install plyfile

# Computer vision
pip install opencv-python opencv-contrib-python
pip install mediapipe
pip install pillow
pip install scikit-image

# Audio processing
pip install librosa soundfile torchaudio
pip install transformers  # For wav2vec
pip install datasets

# 3D models
pip install trimesh
pip install scipy

# Gradio interface
pip install gradio
pip install fastapi uvicorn

# Utilities
pip install tqdm pyyaml wandb
pip install matplotlib plotly

echo "📥 Cloning essential repositories..."

# Create workspace for external repos
mkdir -p external
cd external

# 1. Gaussian Splatting Rasterizer
echo "Installing diff-gaussian-rasterization..."
git clone https://github.com/graphdeco-inria/diff-gaussian-rasterization.git
cd diff-gaussian-rasterization
pip install -e .
cd ..

# 2. GaussianAvatar (primary 3DGS avatar method)
echo "Cloning GaussianAvatar..."
git clone https://github.com/huliangxiao/GaussianAvatar.git

# 3. Wav2Lip (fallback/baseline)
echo "Cloning Wav2Lip..."
git clone https://github.com/Rudrabha/Wav2Lip.git
cd Wav2Lip
pip install -r requirements.txt
cd ..

# 4. GFPGAN (face enhancement)
echo "Cloning GFPGAN..."
git clone https://github.com/TencentARC/GFPGAN.git
cd GFPGAN
pip install -r requirements.txt
python setup.py develop
cd ..

# 5. TTS - Coqui TTS
echo "Installing TTS engine..."
pip install TTS

cd ..  # Back to project root

echo "🧪 Verifying installation..."
python - << 'PYTHON_SCRIPT'
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

import cv2
print(f"OpenCV version: {cv2.__version__}")

import librosa
print(f"Librosa version: {librosa.__version__}")

import gradio as gr
print(f"Gradio version: {gr.__version__}")

print("\n✅ All core dependencies installed successfully!")
PYTHON_SCRIPT

echo "📝 Creating configuration..."
cat > config.yaml << 'EOF'
# TalkingAvatar-3DGS Configuration

project:
  name: "talking-avatar-3dgs"
  output_dir: "./outputs"

gaussian_avatar:
  resolution: 512
  num_iterations: 30000
  position_lr: 0.00016
  feature_lr: 0.0025
  opacity_lr: 0.05
  scaling_lr: 0.005
  rotation_lr: 0.001

audio:
  sample_rate: 16000
  tts_model: "tts_models/en/ljspeech/tacotron2-DDC"

rendering:
  fps: 25
  resolution: [512, 512]

interface:
  host: "0.0.0.0"
  port: 7860
EOF

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place your training video in data/raw/training_video.mp4"
echo "2. Place voice reference in data/raw/voice_reference.wav"
echo "3. Run: python scripts/test_components.py"
echo ""
echo "To start Gradio interface:"
echo "python src/interface/app.py"
