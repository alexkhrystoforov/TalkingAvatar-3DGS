# TalkingAvatar-3DGS

End-to-End Talking Head Generation with 3D Gaussian Splatting

## Quick Start

### Local Development (macOS)
This project requires GPU. Development is done locally, training/rendering on RunPod.

```bash
# Install local dependencies (for development/interface only)
pip install -r requirements-local.txt
```

### RunPod Setup
1. Launch RunPod instance (A6000 or A100 recommended)
2. SSH into instance
3. Run setup:
```bash
git clone <your-repo>
cd TalkingAvatar-3DGS
bash setup_runpod.sh
```

## Architecture
Text → TTS → Audio Features → Motion Parameters → 3DGS Avatar Animation → Video

## Project Status
- [ ] Phase 1: Foundation & Baseline (Days 1-2)
- [ ] Phase 2: 3DGS Avatar Training (Days 3-4)
- [ ] Phase 3: Audio-Driven Animation (Days 5-6)
- [ ] Phase 4: Polish & Interface (Day 7)

## Documentation
See [CLAUDE.md](CLAUDE.md) for detailed project plan and architecture.
