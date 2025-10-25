# RunPod Setup Guide - TalkingAvatar-3DGS

Complete guide for setting up the TalkingAvatar-3DGS project on RunPod with Wav2Lip and SadTalker.

## 🚀 Quick Start

### 1. Deploy RunPod Instance

**Recommended Template:**
- **PyTorch 2.4.0**: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`
- **GPU**: A6000 (48GB) or A100
- **Storage**: 50GB Network Volume (for persistence)
- **Ports**: Expose 7860 (Gradio interface)

### 2. Initial Setup

```bash
# Connect via SSH or use RunPod web terminal
# Clone the repository
cd /workspace
git clone https://github.com/<your-username>/TalkingAvatar-3DGS.git
cd TalkingAvatar-3DGS

# Configure git (for committing changes later)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📦 Install Dependencies

### Core Dependencies

```bash
# Install system packages
apt-get update
apt-get install -y ffmpeg git wget

# Install minimal Python requirements
pip install --no-cache-dir -r requirements_minimal.txt
```

**requirements_minimal.txt:**
```
# Core
numpy>=1.24.0
scipy>=1.10.0

# Computer Vision
opencv-python>=4.8.0
pillow>=10.0.0

# Audio Processing
librosa==0.9.1
soundfile>=0.12.0

# Face Detection
face-alignment>=1.3.5

# Web Interface
gradio>=3.50.0

# Utilities
tqdm>=4.65.0
ninja>=1.11.0
gdown
```

## 🎬 Setup Wav2Lip

### 1. Clone Wav2Lip Repository

```bash
cd /workspace/TalkingAvatar-3DGS
mkdir -p external
cd external
git clone https://github.com/Rudrabha/Wav2Lip.git
```

### 2. Skip Wav2Lip Requirements

**IMPORTANT:** Don't install Wav2Lip's `requirements.txt` - it has outdated dependencies that conflict with Python 3.11!

The dependencies we installed earlier (opencv, librosa 0.9.1, etc.) are sufficient.

### 3. Download Wav2Lip Checkpoint

```bash
cd /workspace/TalkingAvatar-3DGS/external/Wav2Lip
mkdir -p checkpoints
cd checkpoints

# Download via Google Drive (preferred method)
pip install gdown
gdown 15G3U08c8xsCkOqQxE38Z2XXDnPcOptNk -O wav2lip_gan.pth

# Verify download (should be ~140MB)
ls -lh wav2lip_gan.pth
```

### 4. Fix PyTorch Compatibility

Edit `inference.py` to work with PyTorch 2.4+:

```bash
# Add weights_only=False to torch.load
sed -i 's/checkpoint = torch.load(checkpoint_path)/checkpoint = torch.load(checkpoint_path, weights_only=False)/g' /workspace/TalkingAvatar-3DGS/external/Wav2Lip/inference.py
```

### 5. Test Wav2Lip

```bash
cd /workspace/TalkingAvatar-3DGS
python scripts/baseline_wav2lip.py \
  --video /workspace/TalkingAvatar-3DGS/data/raw/training_video.mp4 \
  --audio /workspace/TalkingAvatar-3DGS/data/raw/voice_reference.wav \
  --output /workspace/TalkingAvatar-3DGS/outputs/videos/test_wav2lip.mp4
```

## 🎨 Setup SadTalker

### 1. Clone SadTalker Repository

```bash
cd /workspace/TalkingAvatar-3DGS/external
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
```

### 2. Install SadTalker Dependencies

```bash
# Install requirements (may take 5-10 minutes)
pip install --no-cache-dir -r requirements.txt
```

**Common Issues & Fixes:**

**Issue 1: `scikit-image` building from source (slow)**
- This is normal, wait 5-10 minutes for it to compile

**Issue 2: `torchvision.transforms.functional_tensor` import error**
```bash
# Fix the import path
sed -i "s/functional_tensor/functional/g" /usr/local/lib/python3.11/dist-packages/basicsr/data/degradations.py
```

**Issue 3: `imageio` recursion error**
```bash
# Reinstall imageio with specific version
pip uninstall -y imageio imageio-ffmpeg
pip install --no-cache-dir imageio==2.31.1 imageio-ffmpeg
```

### 3. Download SadTalker Models

```bash
cd /workspace/TalkingAvatar-3DGS/external/SadTalker
bash scripts/download_models.sh
```

This downloads:
- Face detection models
- 3DMM models
- Animation models
- Total: ~2-3GB

### 4. Test SadTalker

```bash
cd /workspace/TalkingAvatar-3DGS/external/SadTalker
python inference.py \
  --driven_audio /workspace/TalkingAvatar-3DGS/data/raw/voice_reference.wav \
  --source_image /workspace/TalkingAvatar-3DGS/data/raw/training_video.mp4 \
  --result_dir /workspace/TalkingAvatar-3DGS/outputs/videos/ \
  --enhancer gfpgan
```

## 🌐 Launch Web Interface

### Start Gradio Interface

```bash
cd /workspace/TalkingAvatar-3DGS
python src/interface/app.py
```

The interface will start on port 7860.

### Access Methods

**Option 1: RunPod Port Mapping**
- Go to RunPod dashboard → Your Pod
- Find "TCP Port Mappings"
- Look for port 7860 mapping
- Access via: `https://xxxxx-7860.proxy.runpod.net`

**Option 2: Gradio Share Link (Temporary)**
- The app is configured with `share=True`
- A public `https://xxxxx.gradio.live` URL will be shown in terminal
- Valid for 72 hours

**Option 3: Direct IP (if port is exposed)**
- `http://<runpod-ip>:7860`

## 📁 Upload Training Data

From your local machine:

```bash
# Upload video
scp -P <port> -i ~/.ssh/id_ed25519 \
  data/raw/training_video.mp4 \
  root@<runpod-ip>:/workspace/TalkingAvatar-3DGS/data/raw/

# Upload audio
scp -P <port> -i ~/.ssh/id_ed25519 \
  data/raw/voice_reference.wav \
  root@<runpod-ip>:/workspace/TalkingAvatar-3DGS/data/raw/
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Wav2Lip checkpoint downloaded (~140MB)
- [ ] SadTalker models downloaded (~2-3GB)
- [ ] Training data uploaded (video + audio)
- [ ] Wav2Lip test generates video successfully
- [ ] SadTalker test generates video successfully
- [ ] Gradio interface accessible via browser
- [ ] Can upload files and generate videos via web UI

## 🐛 Troubleshooting

### Wav2Lip Issues

**"EOFError: Ran out of input"**
- Checkpoint corrupted, re-download with gdown

**"torch.load TorchScript error"**
- Add `weights_only=False` to `inference.py` line 162

**"librosa.filters.mel() error"**
- Downgrade: `pip install librosa==0.9.1`

### SadTalker Issues

**"functional_tensor import error"**
- Run the sed command to fix basicsr import

**"imageio RecursionError"**
- Reinstall imageio 2.31.1

**GFPGAN not working**
- It's optional, remove `--enhancer gfpgan` flag

### General Issues

**Out of disk space**
```bash
# Clean up
pip cache purge
apt-get clean
rm -rf /tmp/*
```

**GPU not detected**
```bash
# Check CUDA
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

## 💾 Persistence Tips

Since RunPod pods are temporary:

1. **Use Network Volume** - All data in `/workspace/<volume-name>` persists
2. **Commit changes to GitHub regularly**
3. **Keep training data in Network Volume**
4. **Models download to Network Volume** (checkpoints, SadTalker models)

## 🔄 Starting Fresh Pod

If you need to restart with a new pod:

```bash
# 1. Deploy new pod with same Network Volume attached
# 2. Everything is already there!
cd /workspace/TalkingAvatar-3DGS
python src/interface/app.py
# Done!
```

## 📊 Resource Usage

**Disk Space:**
- Base project: ~500MB
- Wav2Lip checkpoint: ~140MB
- SadTalker models: ~2-3GB
- Dependencies: ~2GB
- **Total: ~5-6GB**

**GPU Memory (during inference):**
- Wav2Lip: ~2-4GB
- SadTalker: ~4-8GB

**Processing Time (30s video):**
- Wav2Lip: ~30-60 seconds
- SadTalker: ~2-5 minutes

---

## 🎯 Quick Reference Commands

```bash
# Start web interface
python src/interface/app.py

# Test Wav2Lip
python scripts/baseline_wav2lip.py --video <video> --audio <audio> --output <output>

# Test SadTalker
cd external/SadTalker && python inference.py --driven_audio <audio> --source_image <video> --result_dir ../../outputs/videos/

# Check GPU
nvidia-smi

# Free up space
pip cache purge && apt-get clean
```

---

**Created for TalkingAvatar-3DGS Project**

🤖 Built with Claude Code
