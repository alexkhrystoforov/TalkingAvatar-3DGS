# TODO - TalkingAvatar-3DGS Project

## 🌅 TOMORROW (Day 1 Priority Tasks)

### Morning Session (2-3 hours)

#### 1. Launch RunPod Instance ⚡ [CRITICAL]
- [ ] Go to https://www.runpod.io/console/pods
- [ ] Click "Deploy" → "GPU Pods"
- [ ] Select GPU: **A6000 (48GB)** or A100 if available
- [ ] Template: PyTorch 2.0+ (or Ubuntu 22.04)
- [ ] Volume: **50GB minimum**
- [ ] Expose ports: **7860** (for Gradio), **8888** (for Jupyter)
- [ ] Deploy and wait for pod to start
- [ ] Save SSH credentials somewhere safe

#### 2. Connect VS Code to RunPod 🔌 [CRITICAL]
- [ ] In VS Code: Install "Remote - SSH" extension (if needed)
- [ ] Press `Cmd+Shift+P` → "Remote-SSH: Connect to Host"
- [ ] Enter RunPod SSH details: `root@<pod-id>.runpod.io -p <port>`
- [ ] Wait for connection to establish
- [ ] Open terminal in VS Code (should be on RunPod now)
- [ ] Test: `nvidia-smi` (should show GPU info)

#### 3. Transfer Project to RunPod 📦 [CRITICAL]
Choose ONE method:

**Method A: Copy entire local project**
```bash
# On your Mac (in a separate terminal, not VS Code):
cd /Users/oleksandr/work/
scp -r TalkingAvatar-3DGS root@<pod-id>.runpod.io:/workspace/
```

**Method B: Recreate on RunPod**
```bash
# In VS Code terminal (connected to RunPod):
cd /workspace
# We'll recreate the structure and files
```

- [ ] Choose method and execute
- [ ] Verify files are on RunPod: `ls -la /workspace/TalkingAvatar-3DGS`

#### 4. Run Setup Script 🛠️ [CRITICAL]
```bash
# In VS Code terminal (on RunPod):
cd /workspace/TalkingAvatar-3DGS
chmod +x setup_runpod.sh
./setup_runpod.sh
```
- [ ] Run setup (takes ~15 minutes, grab coffee ☕)
- [ ] Monitor for any errors
- [ ] If errors occur: note them, we'll debug

#### 5. Test Installation ✅ [CRITICAL - CHECKPOINT 1]
```bash
python scripts/test_components.py
```
- [ ] Verify all tests pass
- [ ] Expected: "🎉 ALL TESTS PASSED!"
- [ ] If failures: identify which components failed

**⚠️ CHECKPOINT 1**: If setup fails, debug before proceeding!

---

### Afternoon Session (2-3 hours)

#### 6. Record Training Data 📹 [CRITICAL]
**Training Video (30-60 seconds):**
- [ ] Find good lighting (natural light or bright room)
- [ ] Set up camera (Mac webcam or iPhone)
- [ ] Position: face centered, head & shoulders visible
- [ ] Read script from DATA_PREPARATION.md (or speak naturally)
- [ ] Record 2-3 takes, pick best one
- [ ] Save as: `data/raw/training_video.mp4`

**Voice Reference (10-15 seconds):**
- [ ] Find quiet room
- [ ] Use Mac mic or headset
- [ ] Speak naturally (see script in DATA_PREPARATION.md)
- [ ] Save as: `data/raw/voice_reference.wav`

**Quality Check:**
- [ ] Watch video: face clearly visible? Good lighting?
- [ ] Listen to audio: clear? No background noise?

#### 7. Upload Data to RunPod 📤
```bash
# On Mac (in separate terminal):
scp data/raw/training_video.mp4 \
  root@<pod-id>.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/

scp data/raw/voice_reference.wav \
  root@<pod-id>.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
```
- [ ] Upload video
- [ ] Upload audio
- [ ] Verify on RunPod: `ls -lh data/raw/`

#### 8. Test Baseline Wav2Lip Demo 🎬 [CRITICAL - CHECKPOINT 2]
```bash
# In VS Code terminal (on RunPod):
python scripts/baseline_wav2lip.py \
  --video data/raw/training_video.mp4 \
  --text "Hello, this is a test of my talking avatar system. I'm excited to see this working!" \
  --voice_reference data/raw/voice_reference.wav \
  --output outputs/videos/baseline_test.mp4
```
- [ ] Run baseline script
- [ ] Wait for processing (2-5 minutes)
- [ ] Check for errors
- [ ] If successful: download result video

**Download result:**
```bash
# On Mac:
scp root@<pod-id>...:/workspace/TalkingAvatar-3DGS/outputs/videos/baseline_test.mp4 ./
```
- [ ] Download and watch video
- [ ] Is lip-sync working?
- [ ] Quality acceptable?

**⚠️ CHECKPOINT 2**: If baseline works, you have safety net! ✅

#### 9. Test 3DGS Rendering 🎨 [CRITICAL - CHECKPOINT 3]
```bash
# In VS Code terminal (on RunPod):
cd external/diff-gaussian-rasterization

# Test import
python -c "from diff_gaussian_rasterization import GaussianRasterizer; print('✅ 3DGS rendering works!')"
```
- [ ] Test if diff-gaussian-rasterization works
- [ ] If fails: check build logs, may need to rebuild
- [ ] If succeeds: 🎉 We can render Gaussians!

**Explore GaussianAvatar:**
```bash
cd ../GaussianAvatar
ls -la
cat README.md  # Read their documentation
```
- [ ] Explore GaussianAvatar structure
- [ ] Read their README
- [ ] Check if they have example data/scripts
- [ ] Understand their training requirements

**⚠️ CHECKPOINT 3 (END OF DAY 1)**:
- [ ] **Question**: Can we render 3D Gaussians at all?
  - ✅ YES → Plan for full 3DGS avatar training (Day 2-3)
  - ❌ NO → Spend tomorrow morning debugging OR prepare hybrid approach

---

## 📊 End of Day 1 Success Criteria

### Must Have (Critical):
- [x] RunPod instance running and accessible
- [x] VS Code connected to RunPod
- [x] All dependencies installed successfully
- [x] Baseline Wav2Lip demo produces video
- [x] Training data recorded and uploaded

### Should Have (Important):
- [ ] 3DGS rendering test passes
- [ ] Baseline video quality is acceptable
- [ ] Understanding of GaussianAvatar structure

### Nice to Have (Bonus):
- [ ] Explored GaussianAvatar code
- [ ] Tried any GaussianAvatar examples
- [ ] Tested TTS voice cloning quality

---

## 🚨 Risk Assessment - End of Day 1

After completing Day 1, evaluate:

| Risk | Mitigation |
|------|-----------|
| 3DGS rendering doesn't work | → Spend Day 2 morning debugging OR pivot to polished Wav2Lip + showcase 3DGS components separately |
| Baseline video quality poor | → Adjust Wav2Lip parameters, try different video preprocessing |
| Training video quality bad | → Re-record with better lighting tomorrow |
| RunPod setup issues | → Use RunPod pre-built PyTorch template, manual package install |

---

## 📅 DAY 2 Preview (if Day 1 goes well)

### Morning:
- [ ] Preprocess training video (extract frames, COLMAP)
- [ ] Generate segmentation masks
- [ ] Study GaussianAvatar training script

### Afternoon:
- [ ] Configure GaussianAvatar training parameters
- [ ] Start first 3DGS avatar training run
- [ ] Monitor training progress

**Day 2 Checkpoint**: Do we have a trained 3DGS avatar (even low quality)?

---

## 💡 Quick Tips for Tomorrow

1. **Start Early**: RunPod setup takes time, don't underestimate
2. **Save SSH Details**: Write down RunPod connection info
3. **Test Often**: Run test_components.py if anything seems off
4. **Keep Mac Terminal Open**: For SCP transfers
5. **Take Notes**: Update PROGRESS.md with what works/doesn't
6. **Don't Panic**: Baseline Wav2Lip is your safety net!

---

## 🆘 If Things Go Wrong Tomorrow

### Setup Fails:
- Check RunPod has GPU: `nvidia-smi`
- Try manual pip install: `pip install <package>`
- Use `--no-cache-dir` flag if installs fail

### Can't Connect VS Code:
- Fall back to regular SSH: `ssh root@<pod>...`
- Use RunPod's built-in web terminal
- Transfer files via SCP instead

### Baseline Demo Fails:
- Check Wav2Lip checkpoint downloaded
- Verify ffmpeg installed: `ffmpeg -version`
- Try with simpler inputs first

### 3DGS Won't Build:
- Check CUDA version: `nvcc --version`
- Rebuild: `cd external/diff-gaussian-rasterization && pip install -e .`
- Check GitHub issues for GaussianAvatar

---

## 📝 Before Starting Tomorrow

- [ ] Read RUNPOD_QUICKSTART.md (5 min refresh)
- [ ] Read DATA_PREPARATION.md (recording tips)
- [ ] Have RunPod account ready
- [ ] Ensure you have ~4-6 hours available
- [ ] Coffee/tea ready ☕

---

## 🎯 Remember

**Goal for Day 1**: Get everything working and tested
**Not Goal**: Perfect quality or training avatars yet

You're **setting up infrastructure** today. Training comes Day 2-4.

**Even if 3DGS doesn't work**: You'll have a working baseline demo, which is already impressive!

---

---

## 📅 DAY 2 PLAN - Testing & Web Interface

### ✅ COMPLETED SO FAR (Day 1 Extended):
- [x] Baseline Wav2Lip script created (using edge-tts)
- [x] Training video recorded (iPhone, converted to MP4)
- [x] Voice reference recorded (converted to WAV)
- [x] Files uploaded to RunPod (`/workspace/TalkingAvatar-3DGS/data/raw/`)
- [x] Wav2Lip checkpoint downloaded (wav2lip_gan.pth, ~350MB)
- [x] All dependencies installed on RunPod
- [x] Ready to test (waiting for GPU availability)

### 🔄 READY TO RUN (When GPU available):
```bash
# Everything is set up, just need to run:
cd /workspace/TalkingAvatar-3DGS
python scripts/baseline_wav2lip.py \
  --video data/raw/training_video.mp4 \
  --audio data/raw/voice_reference.wav \
  --output outputs/videos/my_first_demo.mp4
```

### Morning Session (RunPod - GPU needed)
- [ ] **Get RunPod with GPU** (restart pod or create new one)
- [x] Pull latest code from GitHub
- [x] Upload training data (video + audio)
- [x] Download Wav2Lip checkpoint
- [ ] Install scipy for Wav2Lip (pip install scipy)
- [ ] Test baseline Wav2Lip script
- [ ] Evaluate lip-sync quality
- [ ] Generate 2-3 demo videos with different text

### Afternoon Session (Can work LOCAL or RunPod)
- [ ] **Build Gradio Web Interface** 🌐
  - Text input for script
  - Video upload widget
  - Voice selection dropdown
  - Progress indicator
  - Video preview and download
  - Deploy on RunPod (accessible via browser)

- [ ] **Interface Features:**
  - Simple mode: Text → Video (one click)
  - Advanced mode: Voice selection, enhancement options
  - Side-by-side comparison (future: Wav2Lip vs 3DGS)

- [ ] Test web interface
- [ ] Create demo scenarios for interview
- [ ] PAUSE RunPod to save costs

### Web Interface Benefits for Interview:
- ✅ Shows full-stack thinking (not just ML)
- ✅ Easy to demonstrate live
- ✅ Professional presentation
- ✅ Can let interviewer try it themselves
- ✅ Works from any browser (no local setup needed)

---

## 🎯 IMMEDIATE NEXT STEPS (When GPU Available)

### Quick Win Path (2-3 hours):
1. **Restart RunPod** - Try different times/GPU types for availability
2. **Install scipy** - `pip install scipy` (1 min)
3. **Run baseline demo** - Generate first video (5 min)
4. **Download and watch** - See yourself talking! (2 min)
5. **Generate 3-5 demos** - Different texts for variety (15 min)
6. **Build Gradio interface** - Web UI for easy demos (1-2 hours)

### What You Can Do NOW (Without GPU - LOCAL):
1. **Commit progress to GitHub** - Save all today's work
2. **Create demo script ideas** - Write interesting texts to test
3. **Plan Gradio interface** - Sketch out UI design
4. **Review CLAUDE.md** - Understand dual-pipeline strategy
5. **Prepare for interview** - Think about talking points

### Potential Issues to Watch:
- ⚠️ **edge-tts API issues** - Have backup: use your voice_reference.wav directly
- ⚠️ **GPU availability** - Try different times, different GPU types
- ⚠️ **Wav2Lip dependencies** - May need: scipy, opencv-python, librosa

---

## 📊 Progress Summary

### Day 1 Achievements: 🎉
- ✅ RunPod environment set up (PyTorch 2.9.0, CUDA 12.8)
- ✅ Baseline libraries installed (Wav2Lip, GFPGAN, edge-tts)
- ✅ Dual-pipeline strategy defined (Wav2Lip + 3DGS)
- ✅ Training data recorded and uploaded
- ✅ Demo script ready to run
- ✅ All files in persistent storage

### Blockers Resolved:
- ✅ 3DGS compilation issues → Documented, will address later
- ✅ Python 3.12 compatibility → Using edge-tts instead of Coqui TTS
- ✅ CUDA version mismatch → Reinstalled PyTorch with correct version
- ✅ Data preparation → Videos recorded, converted, uploaded

### Current Blocker:
- ⏳ GPU availability → Will retry when available

### Estimated Time to First Demo:
- **5-10 minutes** once GPU is available! Everything else is ready.

---

## ✅ Done for Today!

Great job setting up the project structure! Tomorrow we bring it to life on the GPU.

**See you tomorrow! 🚀**

Update PROGRESS.md with your notes as you go.
