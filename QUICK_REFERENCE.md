# Quick Reference Card

## 🚀 Common Commands

### RunPod Setup
```bash
# Initial setup
git clone <your-repo>
cd TalkingAvatar-3DGS
./setup_runpod.sh

# Test installation
python scripts/test_components.py
```

### Upload Data
```bash
# From Mac to RunPod
scp data/raw/training_video.mp4 root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
scp data/raw/voice_reference.wav root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
```

### Baseline Demo (Wav2Lip)
```bash
python scripts/baseline_wav2lip.py \
  --video data/raw/training_video.mp4 \
  --text "Your text here" \
  --voice_reference data/raw/voice_reference.wav \
  --output outputs/videos/baseline.mp4
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
  --text "Your script here" \
  --avatar outputs/avatars/my_avatar \
  --output outputs/videos/output.mp4
```

### Launch Gradio
```bash
python src/interface/app.py
```

### Monitor GPU
```bash
# Watch GPU usage
watch -n 1 nvidia-smi

# Check specific metrics
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 1
```

---

## 📁 Key File Locations

```
TalkingAvatar-3DGS/
├── data/raw/                    # Put training data here
│   ├── training_video.mp4
│   └── voice_reference.wav
│
├── src/
│   ├── config.py                # Main configuration
│   ├── gaussian_avatar/         # 3DGS implementation
│   ├── audio/                   # TTS and audio processing
│   └── interface/app.py         # Gradio interface
│
├── scripts/
│   ├── test_components.py       # Test installation
│   ├── baseline_wav2lip.py      # Safety net demo
│   ├── train_avatar.py          # Train 3DGS avatar
│   └── generate_video.py        # End-to-end generation
│
├── outputs/
│   ├── avatars/                 # Trained avatars
│   └── videos/                  # Generated videos
│
└── external/                    # Cloned repos (Wav2Lip, etc.)
```

---

## 🔧 Configuration

Edit `src/config.py` or override in scripts:

### 3DGS Training
- `resolution`: 512 (higher = better quality, slower)
- `num_iterations`: 30000 (more = better, ~30min per avatar)
- Learning rates: adjust if training unstable

### Audio
- `sample_rate`: 16000 (standard)
- `tts_model`: Choose TTS engine
- `use_voice_clone`: True/False

### Rendering
- `fps`: 25 (standard video)
- `resolution`: (512, 512)
- `use_face_enhancement`: True (GFPGAN)

---

## 🐛 Troubleshooting

### CUDA Out of Memory
```python
# Reduce in config.py:
resolution = 256  # Instead of 512
batch_size = 1
```

### Wav2Lip Checkpoint Missing
```bash
cd external/Wav2Lip
wget https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA -O checkpoints/wav2lip_gan.pth
```

### Gradio Not Accessible
```bash
# Option 1: SSH tunnel
ssh -L 7860:localhost:7860 root@<pod-id>...

# Option 2: Use share link
# In app.py: demo.launch(share=True)
```

### Training Not Using GPU
```python
# Check in Python:
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

---

## 📊 Performance Targets

- **Avatar Training**: <30 min per avatar
- **Inference Speed**: 15-30 FPS target
- **Lip-Sync Accuracy**: >80%
- **End-to-End Latency**: <5 min for 30s video

---

## 🎯 Checkpoints

### End of Day 2
**Question**: Is basic 3DGS rendering working?
- ✅ YES → Full steam ahead with 3DGS
- ❌ NO → Debug morning of Day 3 OR prepare hybrid

### End of Day 4
**Question**: Trained 3DGS avatar with reasonable quality?
- ✅ YES → Proceed to integration
- ❌ NO → One more training OR showcase separately

### End of Day 6
**Question**: Audio-driven 3DGS animation working?
- ✅ YES → Polish on Day 7
- ❌ NO → Hybrid demo (3DGS + Wav2Lip side-by-side)

---

## 💾 Backup Strategy

```bash
# Download important files from RunPod regularly
scp -r root@<pod>:/workspace/TalkingAvatar-3DGS/outputs ./outputs_backup
scp -r root@<pod>:/workspace/TalkingAvatar-3DGS/models/avatars ./avatars_backup

# Commit code changes daily
git add .
git commit -m "Day X progress"
git push
```

---

## 🎬 Demo Scenarios

1. **Tech Tutorial**: Avatar explains CV concept
2. **Multi-Lingual**: Same avatar, 2-3 languages
3. **Custom Voice**: Clone voice on the spot
4. **Quality Comparison**: 3DGS vs Wav2Lip side-by-side
5. **Live Generation**: Text from interviewer → video

---

## 📱 Quick Links

- RunPod Dashboard: https://www.runpod.io/console/pods
- Project Plan: [CLAUDE.md](CLAUDE.md)
- Progress Tracker: [PROGRESS.md](PROGRESS.md)
- RunPod Guide: [RUNPOD_QUICKSTART.md](RUNPOD_QUICKSTART.md)

---

## ⚡ Emergency Plan

If everything breaks:
1. Wav2Lip baseline is working ✓
2. Show separate 3DGS components
3. Explain approach and challenges
4. Still demonstrates ML/CV knowledge!

**Remember**: Interview success = demonstrating problem-solving, not perfection!
