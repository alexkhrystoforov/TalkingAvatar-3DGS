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

# Custom CSS
custom_css = """
.gradio-container {
    font-family: 'Arial', sans-serif;
    max-width: 1400px;
    margin: auto;
}

.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.main-header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.main-header p {
    font-size: 1.1rem;
    opacity: 0.9;
}

.feature-card {
    background: #f8f9fa;
    border-left: 4px solid #667eea;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}

.tab-nav button {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}

.generate-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    padding: 0.8rem 2rem !important;
}

.footer {
    text-align: center;
    padding: 2rem;
    margin-top: 2rem;
    border-top: 2px solid #e0e0e0;
    color: #666;
}

.status-box {
    font-family: monospace;
    font-size: 0.95rem;
}
"""

def generate_video_wav2lip(video_file, audio_file):
    """Generate video using Wav2Lip"""
    try:
        # Gradio passes file paths as strings
        video_path = video_file if isinstance(video_file, str) else video_file.name
        audio_path = audio_file if isinstance(audio_file, str) else audio_file.name

        output_path = PROJECT_ROOT / "outputs" / "videos" / f"wav2lip_{Path(video_path).stem}.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "python", str(PROJECT_ROOT / "scripts" / "baseline_wav2lip.py"),
            "--video", video_path,
            "--audio", audio_path,
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
        # Gradio passes file paths as strings
        video_path = video_file if isinstance(video_file, str) else video_file.name
        audio_path = audio_file if isinstance(audio_file, str) else audio_file.name

        sadtalker_dir = PROJECT_ROOT / "external" / "SadTalker"
        output_dir = PROJECT_ROOT / "outputs" / "videos"
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "python", str(sadtalker_dir / "inference.py"),
            "--driven_audio", audio_path,
            "--source_image", video_path,
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
with gr.Blocks(title="TalkingAvatar-3DGS Demo", css=custom_css, theme=gr.themes.Soft()) as demo:

    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🎬 TalkingAvatar-3DGS</h1>
        <p>AI-Powered Talking Head Video Generation</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            Powered by 3D Gaussian Splatting • Wav2Lip • SadTalker
        </p>
    </div>
    """)

    # Feature Overview
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML("""
            <div class="feature-card">
                <h3>⚡ Wav2Lip</h3>
                <p>Fast 2D lip-sync generation</p>
                <ul>
                    <li>Quick processing (~30 seconds)</li>
                    <li>Accurate lip synchronization</li>
                    <li>Good for rapid prototyping</li>
                </ul>
            </div>
            """)

        with gr.Column(scale=1):
            gr.HTML("""
            <div class="feature-card">
                <h3>🎨 SadTalker</h3>
                <p>High-quality 3D-aware generation</p>
                <ul>
                    <li>Natural head movements</li>
                    <li>Realistic facial expressions</li>
                    <li>GFPGAN face enhancement</li>
                </ul>
            </div>
            """)

    with gr.Tabs():
        # Wav2Lip Tab
        with gr.Tab("⚡ Wav2Lip (Fast)"):
            gr.Markdown("### Fast 2D Lip-Sync Generation")
            gr.Markdown("*Best for: Quick demos, testing, when speed matters*")
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
        with gr.Tab("🎨 SadTalker (High Quality)"):
            gr.Markdown("### 3D-Aware Realistic Talking Head Generation")
            gr.Markdown("*Best for: Final output, presentations, professional demos*")
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

    # Footer
    gr.HTML("""
    <div class="footer">
        <h3>📖 How to Use</h3>
        <p>1. Choose a method: <strong>Wav2Lip</strong> for speed or <strong>SadTalker</strong> for quality</p>
        <p>2. Upload your <strong>video</strong> (training footage or source image)</p>
        <p>3. Upload your <strong>audio</strong> (the voice/speech to animate)</p>
        <p>4. Click <strong>Generate</strong> and wait for processing</p>
        <p>5. Download your generated talking head video!</p>
        <hr style="margin: 2rem 0; opacity: 0.3;">
        <p style="color: #999; font-size: 0.9rem;">
            <strong>TalkingAvatar-3DGS Project</strong><br>
            Dual-Pipeline Talking Head Generation System<br>
            🤖 Built with Claude Code • Powered by PyTorch & Gradio
        </p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,
        share=True  # Set to True for public link
    )
