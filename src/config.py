"""
Central configuration for TalkingAvatar-3DGS
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Tuple

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
EXTERNAL_DIR = PROJECT_ROOT / "external"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FRAMES_DIR = PROCESSED_DATA_DIR / "frames"
MASKS_DIR = PROCESSED_DATA_DIR / "masks"
COLMAP_DIR = PROCESSED_DATA_DIR / "colmap"

# Output subdirectories
AVATARS_DIR = OUTPUT_DIR / "avatars"
VIDEOS_DIR = OUTPUT_DIR / "videos"
DEMOS_DIR = OUTPUT_DIR / "demos"

@dataclass
class GaussianAvatarConfig:
    """Configuration for 3DGS avatar training"""
    resolution: int = 512
    num_iterations: int = 30000
    batch_size: int = 1

    # Learning rates
    position_lr: float = 0.00016
    feature_lr: float = 0.0025
    opacity_lr: float = 0.05
    scaling_lr: float = 0.005
    rotation_lr: float = 0.001

    # Densification
    densify_from_iter: int = 500
    densify_until_iter: int = 15000
    densification_interval: int = 100
    opacity_reset_interval: int = 3000

    # Regularization
    lambda_dssim: float = 0.2

    # Checkpointing
    checkpoint_interval: int = 5000
    validation_interval: int = 1000

@dataclass
class AudioConfig:
    """Configuration for audio processing"""
    sample_rate: int = 16000
    hop_length: int = 512
    n_mels: int = 80

    # TTS settings
    tts_model: str = "tts_models/en/ljspeech/tacotron2-DDC"
    tts_vocoder: str = "vocoder_models/en/ljspeech/hifigan_v2"

    # Voice cloning
    use_voice_clone: bool = True
    voice_clone_model: str = "tts_models/multilingual/multi-dataset/xtts_v2"

@dataclass
class RenderingConfig:
    """Configuration for rendering"""
    fps: int = 25
    resolution: Tuple[int, int] = (512, 512)
    background_color: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Post-processing
    use_face_enhancement: bool = True
    use_super_resolution: bool = False

    # Video export
    video_codec: str = "libx264"
    video_bitrate: str = "5000k"
    audio_codec: str = "aac"
    audio_bitrate: str = "192k"

@dataclass
class InterfaceConfig:
    """Configuration for Gradio interface"""
    host: str = "0.0.0.0"
    port: int = 7860
    share: bool = False
    debug: bool = False

# Default configurations
GAUSSIAN_AVATAR_CONFIG = GaussianAvatarConfig()
AUDIO_CONFIG = AudioConfig()
RENDERING_CONFIG = RenderingConfig()
INTERFACE_CONFIG = InterfaceConfig()

def ensure_directories():
    """Create all necessary directories"""
    dirs = [
        DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, FRAMES_DIR, MASKS_DIR, COLMAP_DIR,
        MODELS_DIR, MODELS_DIR / "tts", MODELS_DIR / "gfpgan", MODELS_DIR / "wav2vec",
        OUTPUT_DIR, AVATARS_DIR, VIDEOS_DIR, DEMOS_DIR,
        EXTERNAL_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()
    print("✅ All directories created")
    print(f"Project root: {PROJECT_ROOT}")
