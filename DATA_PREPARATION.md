# Data Preparation Guide

## 📹 Training Video Requirements

### Video Specifications
- **Duration**: 30-60 seconds
- **Resolution**: 1080p or higher (will be downsampled to 512x512)
- **Frame Rate**: 25-30 FPS
- **Format**: MP4, AVI, or MOV

### Recording Tips

#### Lighting
- ✅ Bright, even lighting on face
- ✅ Avoid harsh shadows
- ✅ Natural or studio lighting
- ❌ Backlighting (face too dark)
- ❌ Extreme side lighting

#### Camera Setup
- ✅ Fixed camera position (no camera movement)
- ✅ Face centered in frame
- ✅ Head and shoulders visible
- ✅ Neutral background (solid color preferred)
- ❌ Shaky camera
- ❌ Cluttered background

#### Content
- ✅ Speak naturally (full sentences)
- ✅ Include head movements (nodding, turning slightly)
- ✅ Various expressions (neutral, smiling, talking)
- ✅ Different phonemes (say varied sentences)
- ❌ Static pose throughout
- ❌ Extreme head movements (turning away from camera)

#### Example Script to Read
```
Hello, my name is [Your Name]. I'm excited to create a talking avatar
using 3D Gaussian Splatting. This technology allows for realistic
rendering of faces with natural expressions and movements. Today, I'll
demonstrate various expressions, from neutral to smiling, while
speaking clearly. The system will learn to animate my avatar based on
audio input.
```

### Recording Methods

#### Option 1: Mac Built-in Camera
```bash
# Use QuickTime Player:
# 1. Open QuickTime Player
# 2. File → New Movie Recording
# 3. Record your video
# 4. Export as training_video.mp4
```

#### Option 2: iPhone/Smartphone
```
1. Use front-facing camera in good lighting
2. Prop phone at eye level
3. Record video
4. AirDrop/transfer to Mac
5. Convert if needed (see below)
```

#### Option 3: Professional Camera
```
- Use highest quality settings
- Transfer via SD card or cable
- Ensure MP4 format
```

### Video Conversion (if needed)
```bash
# Convert to MP4 with ffmpeg
ffmpeg -i input_video.mov -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k training_video.mp4

# Resize if too large
ffmpeg -i input_video.mp4 -vf scale=1080:1080 -c:a copy training_video.mp4
```

---

## 🎙️ Voice Reference Requirements

### Audio Specifications
- **Duration**: 10-15 seconds (minimum 5 seconds)
- **Sample Rate**: 16kHz or higher
- **Format**: WAV (preferred) or MP3
- **Quality**: Clear, no background noise

### Recording Tips

#### Environment
- ✅ Quiet room (no background noise)
- ✅ Close to microphone
- ✅ Room with soft furnishings (reduces echo)
- ❌ Noisy environment
- ❌ Echo/reverb
- ❌ Wind noise

#### Content
- ✅ Natural speaking voice
- ✅ Same tone as intended for avatar
- ✅ Complete sentences
- ❌ Whispering or shouting
- ❌ Monotone reading

#### Example Script for Voice Reference
```
This is a sample of my natural speaking voice. I'm speaking clearly
and at a comfortable pace. The system will use this to clone my voice
for the talking avatar.
```

### Recording Methods

#### Option 1: Mac Built-in Mic
```bash
# Use QuickTime Player:
# 1. File → New Audio Recording
# 2. Record your voice
# 3. Export as voice_reference.wav
```

#### Option 2: External Microphone
```
- Use USB microphone or headset
- Record in quiet environment
- Save as WAV format
```

#### Option 3: Convert from Video
```bash
# Extract audio from video
ffmpeg -i training_video.mp4 -vn -acodec pcm_s16le \
  -ar 16000 -ac 1 voice_reference.wav
```

### Audio Conversion
```bash
# Convert MP3 to WAV
ffmpeg -i voice_reference.mp3 -ar 16000 -ac 1 voice_reference.wav

# Reduce background noise (basic)
ffmpeg -i voice_reference.wav -af "highpass=f=200, lowpass=f=3000" \
  voice_reference_clean.wav
```

---

## 📁 File Organization

Place your prepared files in:
```
data/raw/
├── training_video.mp4     # Your training video
└── voice_reference.wav    # Your voice sample
```

### File Checklist
Before uploading to RunPod, verify:
- [ ] `training_video.mp4` is 30-60 seconds
- [ ] Video shows face clearly with good lighting
- [ ] Face is centered and camera is stable
- [ ] Video includes speech and natural movements
- [ ] `voice_reference.wav` is 10-15 seconds
- [ ] Audio is clear with no background noise
- [ ] Both files are in correct format
- [ ] File names match exactly (important for scripts)

---

## 🔍 Quality Check

### Video Quality Check
```bash
# Get video info
ffmpeg -i data/raw/training_video.mp4

# Should show:
# - Duration: 30-60s
# - Resolution: at least 720p
# - Frame rate: 25-30 fps
```

### Audio Quality Check
```bash
# Get audio info
ffmpeg -i data/raw/voice_reference.wav

# Should show:
# - Duration: 10-15s
# - Sample rate: 16000 Hz or higher
# - Channels: 1 (mono) or 2 (stereo)
```

### Visual Inspection
```bash
# Play video to check quality
# On Mac: open data/raw/training_video.mp4

# Play audio to check quality
# On Mac: open data/raw/voice_reference.wav
```

---

## 📤 Uploading to RunPod

Once your files are ready:

```bash
# Upload video
scp data/raw/training_video.mp4 \
  root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/

# Upload audio
scp data/raw/voice_reference.wav \
  root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
```

Or use rsync for faster transfer:
```bash
rsync -avz --progress data/raw/ \
  root@<pod-id>.pods.runpod.io:/workspace/TalkingAvatar-3DGS/data/raw/
```

---

## ⚡ Quick Start Examples

### Example 1: Use Training Video Audio
If your training video has good audio:
```bash
# Extract audio from video
ffmpeg -i data/raw/training_video.mp4 -vn -ar 16000 \
  data/raw/voice_reference.wav
```

### Example 2: Test with Sample Media
For initial testing without recording:
```bash
# Download test video (placeholder)
# You can use any video temporarily for testing setup
```

---

## 🎯 Pro Tips

1. **Multiple Takes**: Record 3-4 videos, pick the best one
2. **Consistency**: Use same lighting/background if training multiple avatars
3. **Backup**: Keep original high-quality files, create working copies
4. **File Size**: Keep video under 500MB for faster upload
5. **Preview**: Always review your recordings before processing

---

## 🐛 Common Issues

### Video too dark
```bash
# Brighten video
ffmpeg -i input.mp4 -vf "eq=brightness=0.06:saturation=1.3" output.mp4
```

### Audio has noise
```bash
# Basic noise reduction
ffmpeg -i input.wav -af "highpass=f=200,lowpass=f=3000" output.wav
```

### File too large
```bash
# Compress video
ffmpeg -i input.mp4 -crf 23 -preset medium output.mp4

# Compress audio
ffmpeg -i input.wav -ar 16000 -ac 1 output.wav
```

### Wrong format
```bash
# Convert video to MP4
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4

# Convert audio to WAV
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
```

---

## ✅ Ready to Go!

Once you have:
- ✅ training_video.mp4 (30-60s, good quality, face visible)
- ✅ voice_reference.wav (10-15s, clear audio)

You're ready to:
1. Upload to RunPod
2. Run the baseline demo
3. Train your 3DGS avatar

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for next steps!
