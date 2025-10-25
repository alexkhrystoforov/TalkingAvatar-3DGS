#!/usr/bin/env python3
"""
Gradio Web Interface for TalkingAvatar-3DGS
Supports both Wav2Lip and SadTalker pipelines
"""

import gradio as gr
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def generate_video_wav2lip(video_file, audio_file):
    """Generate video using Wav2Lip"""
    try:
        output_path = PROJECT_ROOT / "outputs" / "videos" / f"wav2lip_{Path(video_file.name).stem}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "python", str(PROJECT_ROOT / "scripts" / "baseline_wav2lip.py"),
            "--video", video_file.name,
            "--audio", audio_file.name,
            "--output", str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and output_path.exists():
            return str(output_path), "✅ Wav2Lip generation successful!"
        else:
            return None, f"❌ Error: {result.stderr}"
    except Exception as e:
        return None, f"❌ Exception: {str(e)}"

def generate_video_sadtalker(video_file, audio_file, use_enhancer=True):
    """Generate video using SadTalker"""
    try:
        sadtalker_dir = PROJECT_ROOT / "external" / "SadTalker"
        output_dir = PROJECT_ROOT / "outputs" / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "python", str(sadtalker_dir / "inference.py"),
            "--driven_audio", audio_file.name,
            "--source_image", video_file.name,
            "--result_dir", str(output_dir),
        ]

        if use_enhancer:
            cmd.append("--enhancer")
            cmd.append("gfpgan")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=sadtalker_dir)

        # Find the generated video (SadTalker names it with timestamp)
        videos = sorted(output_dir.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)

        if videos:
            return str(videos[0]), "✅ SadTalker generation successful!"
        else:
            return None, f"❌ Error: {result.stderr}"
    except Exception as e:
        return None, f"❌ Exception: {str(e)}"

# Gradio Interface
with gr.Blocks(title="TalkingAvatar-3DGS Demo") as demo:
    gr.Markdown("""
    # 🎬 TalkingAvatar-3DGS Demo

    Generate talking head videos using **Wav2Lip** or **SadTalker**

    - **Wav2Lip**: Fast, good lip-sync (2D)
    - **SadTalker**: Better quality, natural head movements (3D-aware)
    """)

    with gr.Tabs():
        # Wav2Lip Tab
        with gr.Tab("Wav2Lip (Fast)"):
            gr.Markdown("### Upload video and audio to generate lip-synced video")
            with gr.Row():
                with gr.Column():
                    wav2lip_video = gr.Video(label="Input Video")
                    wav2lip_audio = gr.Audio(label="Input Audio", type="filepath")
                    wav2lip_btn = gr.Button("Generate with Wav2Lip", variant="primary")

                with gr.Column():
                    wav2lip_output = gr.Video(label="Generated Video")
                    wav2lip_status = gr.Textbox(label="Status", lines=2)

            wav2lip_btn.click(
                fn=generate_video_wav2lip,
                inputs=[wav2lip_video, wav2lip_audio],
                outputs=[wav2lip_output, wav2lip_status]
            )

        # SadTalker Tab
        with gr.Tab("SadTalker (High Quality)"):
            gr.Markdown("### Upload image/video and audio for realistic talking head")
            with gr.Row():
                with gr.Column():
                    sadtalker_video = gr.Video(label="Input Video/Image")
                    sadtalker_audio = gr.Audio(label="Input Audio", type="filepath")
                    sadtalker_enhancer = gr.Checkbox(label="Use GFPGAN Face Enhancement", value=True)
                    sadtalker_btn = gr.Button("Generate with SadTalker", variant="primary")

                with gr.Column():
                    sadtalker_output = gr.Video(label="Generated Video")
                    sadtalker_status = gr.Textbox(label="Status", lines=2)

            sadtalker_btn.click(
                fn=generate_video_sadtalker,
                inputs=[sadtalker_video, sadtalker_audio, sadtalker_enhancer],
                outputs=[sadtalker_output, sadtalker_status]
            )

    gr.Markdown("""
    ---
    **Created for TalkingAvatar-3DGS Project**

    🤖 Generated with [Claude Code](https://claude.com/claude-code)
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,
        share=False  # Set to True for public link
    )
