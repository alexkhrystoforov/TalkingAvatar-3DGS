# RunPod Quick Start Guide

## 1. Launch RunPod Instance

### Recommended Configuration:
- **GPU**: A6000 (48GB VRAM) or A100 (40GB/80GB)
- **Template**: PyTorch 2.0+ with CUDA 11.8+
- **Storage**: At least 50GB for models and outputs
- **Ports**: Expose port 7860 for Gradio interface

### Steps:
1. Go to https://www.runpod.io/
2. Click "Deploy" → "GPU Pods"
3. Select GPU (A6000 recommended for cost/performance)
4. Choose PyTorch template (or Ubuntu + Docker)
5. Set volume size: 50GB minimum
6. Deploy pod

## 2. SSH into RunPod

```bash
# RunPod will give you SSH command, something like:
ssh root@<pod-id>.pods.runpod.io -p <port> -i ~/.ssh/id_ed25519
```

## 3. Initial Setup

```bash
# Clone your repository (once you push it to GitHub)
git clone https://github.com/<your-username>/TalkingAvatar-3DGS.git
cd TalkingAvatar-3DGS

# Make setup script executable
chmod +x setup_runpod.sh

# Run setup (this takes 10-15 minutes)
./setup_runpod.sh
```

## 4. Test Installation

```bash
# Run component tests
python scripts/test_components.py
```

You should see:
```
🎉 ALL TESTS PASSED! Ready to start development.
```

## 5. Transfer Training Data

### Option A: From your Mac via SCP
```bash
# On your Mac:
scp data/raw/training_video.mp4 root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
scp data/raw/voice_reference.wav root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
```

### Option B: Download from cloud
```bash
# On RunPod:
cd data/raw
wget <your-video-url> -O training_video.mp4
wget <your-audio-url> -O voice_reference.wav
```

### Option C: Record on RunPod
```bash
# If you have a webcam/mic on RunPod (unlikely)
# Or upload via Gradio interface later
```

## 6. Start Jupyter (Optional)

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Then access via RunPod's port forwarding.

## 7. Development Workflow

### Sync code from Mac to RunPod:

**Option 1: Git (recommended)**
```bash
# On Mac: commit and push
git add .
git commit -m "Update code"
git push

# On RunPod: pull
git pull
```

**Option 2: rsync**
```bash
# On Mac:
rsync -avz --exclude='data/' --exclude='outputs/' --exclude='external/' \
  ./ root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/
```

**Option 3: VS Code Remote SSH**
Install "Remote - SSH" extension in VS Code, then connect to RunPod.

## 8. Running the Pipeline

### Test Baseline (Wav2Lip)
```bash
python scripts/baseline_wav2lip.py \
  --video data/raw/training_video.mp4 \
  --audio data/raw/voice_reference.wav \
  --output outputs/videos/baseline_test.mp4
```

### Train 3DGS Avatar
```bash
python scripts/train_avatar.py \
  --video data/raw/training_video.mp4 \
  --name my_avatar \
  --iterations 30000
```

### Generate Video
```bash
python scripts/generate_video.py \
  --text "Hello, this is a test of my talking avatar system." \
  --avatar outputs/avatars/my_avatar \
  --output outputs/videos/test_output.mp4
```

### Launch Gradio Interface
```bash
python src/interface/app.py
```

Then access at: `http://<runpod-ip>:7860`

## 9. Download Results

```bash
# On your Mac:
scp root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/outputs/videos/test_output.mp4 ./
```

## Troubleshooting

### CUDA Out of Memory
- Reduce `resolution` in config
- Reduce `batch_size`
- Use gradient checkpointing

### Slow Training
- Check GPU utilization: `nvidia-smi`
- Ensure you're using GPU instance, not CPU
- Reduce `num_iterations` for testing

### Can't Access Gradio
- Check RunPod port forwarding settings
- Use `share=True` in Gradio for temporary public link
- SSH tunnel: `ssh -L 7860:localhost:7860 root@<pod>...`

### Package Installation Fails
```bash
pip install --no-cache-dir <package>
# or
pip install --force-reinstall <package>
```

## Cost Optimization

- **Stop pod when not in use** (data persists on volume)
- Use A6000 instead of A100 if budget-constrained (still very capable)
- Train multiple avatars in one session to maximize GPU time
- Download important results frequently (pods can be terminated)

## Next Steps

See [CLAUDE.md](CLAUDE.md) for the full project plan and development roadmap.
