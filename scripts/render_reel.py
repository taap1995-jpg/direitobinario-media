#!/usr/bin/env python3
"""Render a vertical Direitobinario MP4 for Instagram Reels with FFmpeg.

Preserves the source's navy/gold visuals and embedded text, converts it to
1080x1920/30 fps, and normalizes audio loudness and intelligibility. It does
not synthesize or replace the speaker's voice.
"""
import argparse
import shutil
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Path to the source MP4")
    parser.add_argument("output", help="Path for the rendered MP4")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg was not found. Install FFmpeg and retry.")

    source = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"Input file does not exist: {source}")
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        ffmpeg, "-hide_banner", "-y", "-i", str(source),
        "-map", "0:v:0", "-map", "0:a:0?",
        "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
        "-af", "aresample=async=1:first_pts=0,highpass=f=75,equalizer=f=2800:t=q:w=1:g=1.2,loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", "-max_muxing_queue_size", "1024",
        str(output),
    ]
    subprocess.run(command, check=True)
    print(f"Rendered: {output}")


if __name__ == "__main__":
    main()
