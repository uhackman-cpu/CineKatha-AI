#!/usr/bin/env python3
"""CineKatha-AI zero-budget, local-first storyboard-to-video MVP.

Creates cinematic still frames, optional local narration, SRT subtitles, and an MP4
using Pillow, espeak-ng/espeak (optional), and FFmpeg (required for MP4).
No network calls, API keys, or paid services are used.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing Pillow. Install with: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

W, H = 1920, 1080
PALETTE = [(12, 20, 38), (26, 25, 48), (14, 35, 48), (37, 24, 42), (17, 29, 55)]


def load_font(size: int, bold: bool = False):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def split_scenes(story: str, max_chars: int = 420) -> list[str]:
    clean = re.sub(r"\s+", " ", story).strip()
    if not clean:
        raise ValueError("Story file is empty.")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", story.strip()) if p.strip()]
    units = paragraphs or [clean]
    scenes: list[str] = []
    for unit in units:
        sentences = re.split(r"(?<=[.!?।])\s+", re.sub(r"\s+", " ", unit))
        current = ""
        for sentence in sentences:
            if not sentence:
                continue
            if current and len(current) + len(sentence) + 1 > max_chars:
                scenes.append(current.strip())
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            scenes.append(current.strip())
    return scenes


def make_frame(index: int, total: int, text: str, out: Path, title: str):
    image = Image.new("RGB", (W, H), PALETTE[(index - 1) % len(PALETTE)])
    draw = ImageDraw.Draw(image, "RGBA")
    # Atmospheric gradients and cinematic letterbox.
    for y in range(H):
        alpha = int(65 * y / H)
        draw.line((0, y, W, y), fill=(0, 0, 0, alpha))
    draw.ellipse((W * .58, -H * .48, W * 1.18, H * .60), fill=(80, 115, 150, 24))
    draw.rectangle((0, 0, W, 105), fill=(0, 0, 0, 150))
    draw.rectangle((0, H - 115, W, H), fill=(0, 0, 0, 175))
    title_font = load_font(38, True)
    body_font = load_font(54)
    small_font = load_font(28)
    draw.text((110, 34), title[:55], font=title_font, fill=(245, 225, 190, 255))
    draw.text((W - 280, 42), f"SCENE {index:02d}/{total:02d}", font=small_font, fill=(210, 220, 235, 230))
    lines = textwrap.wrap(text, width=48)
    lines = lines[:8]
    line_h = 82
    block_h = len(lines) * line_h
    y = (H - block_h) // 2
    draw.rounded_rectangle((95, y - 55, W - 95, y + block_h + 45), radius=28, fill=(0, 0, 0, 95), outline=(230, 210, 175, 90), width=2)
    for line in lines:
        draw.text((145, y), line, font=body_font, fill=(250, 248, 240, 255), stroke_width=1, stroke_fill=(0, 0, 0, 100))
        y += line_h
    draw.text((110, H - 75), "CINEKATHA-AI  •  LOCAL ZERO-BUDGET PREVIEW", font=small_font, fill=(190, 200, 215, 220))
    image.save(out, quality=95)


def run(cmd: list[str], *, check: bool = True, cwd: Path | None = None):
    return subprocess.run(cmd, check=check, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def make_voice(text: str, wav_path: Path, voice: str, rate: int) -> bool:
    engine = shutil.which("espeak-ng") or shutil.which("espeak")
    if not engine:
        return False
    result = subprocess.run([engine, "-v", voice, "-s", str(rate), "-w", str(wav_path), text],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        wav_path.unlink(missing_ok=True)
        return False
    return wav_path.exists() and wav_path.stat().st_size > 44


def srt_time(seconds: float) -> str:
    ms = int(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def build(args):
    source = Path(args.story).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Story file not found: {source}")
    story = source.read_text(encoding="utf-8")
    scenes = split_scenes(story)
    project = Path(args.output).expanduser().resolve()
    frames = project / "frames"
    audio = project / "audio"
    frames.mkdir(parents=True, exist_ok=True)
    audio.mkdir(parents=True, exist_ok=True)

    durations: list[float] = []
    voice_files: list[Path | None] = []
    scene_rows = []
    for i, scene in enumerate(scenes, 1):
        frame = frames / f"scene_{i:03}.png"
        make_frame(i, len(scenes), scene, frame, args.title)
        wav = audio / f"scene_{i:03}.wav"
        has_voice = make_voice(scene, wav, args.voice, args.rate) if not args.no_voice else False
        if has_voice:
            probe = shutil.which("ffprobe")
            if probe:
                try:
                    info = json.loads(run([probe, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(wav)]).stdout)
                    duration = max(float(info["format"]["duration"]), 2.5)
                except Exception:
                    duration = max(len(scene) / 11.0, 4.0)
            else:
                duration = max(len(scene) / 11.0, 4.0)
        else:
            duration = max(len(scene) / 13.0, 4.0)
            wav.unlink(missing_ok=True)
        durations.append(duration)
        voice_files.append(wav if has_voice else None)
        scene_rows.append({"number": i, "text": scene, "frame": str(frame.relative_to(project)),
                           "audio": str(wav.relative_to(project)) if has_voice else None,
                           "duration_seconds": round(duration, 2)})
    # One SRT cue per scene, aligned to the estimated/actual narration duration.
    cursor = 0.0
    srt = []
    for i, (scene, duration) in enumerate(zip(scenes, durations), 1):
        srt.append(f"{i}\n{srt_time(cursor)} --> {srt_time(cursor + duration)}\n{scene}\n")
        cursor += duration
    (project / "subtitles.srt").write_text("\n".join(srt), encoding="utf-8")

    manifest = {
        "project": args.title, "created_at": datetime.now(timezone.utc).isoformat(),
        "source_file": source.name, "scene_count": len(scenes),
        "render": {"width": W, "height": H, "fps": args.fps, "format": "mp4/h264"},
        "voice_engine": "espeak-ng/espeak" if any(voice_files) else "not available / disabled",
        "scenes": scene_rows,
        "notice": "Storyboard frames are typographic placeholders, not AI-generated photorealistic images."
    }
    (project / "project.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print(f"Project assets created at: {project}")
        print("FFmpeg is missing. Install FFmpeg and rerun to render final.mp4.")
        return
    concat = project / "timeline.txt"
    with concat.open("w", encoding="utf-8") as f:
        for row in scene_rows:
            f.write(f"file '{(project / row['frame']).as_posix()}'\n")
            f.write(f"duration {row['duration_seconds']}\n")
        f.write(f"file '{(project / scene_rows[-1]['frame']).as_posix()}'\n")
    silent_video = project / "silent.mp4"
    run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
         "-vf", f"fps={args.fps},scale=1920:1080,format=yuv420p",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-an", str(silent_video)])

    # Assemble narration in original scene order; subtitle paths resolve from project cwd.
    if any(voice_files):
        inputs = []
        filters = []
        voice_indexes = []
        input_index = 0
        for idx, wav in enumerate(voice_files):
            if wav:
                inputs += ["-i", str(wav)]
                delay = int(sum(durations[:idx]) * 1000)
                filters.append(f"[{input_index}:a]adelay={delay}|{delay}[voice{idx}]")
                voice_indexes.append(f"[voice{idx}]")
                input_index += 1
        graph = ";".join(filters) + ";" + "".join(voice_indexes) + f"amix=inputs={len(voice_indexes)}:normalize=0[aout]"
        try:
            run([ffmpeg, "-y", *inputs, "-filter_complex", graph, "-map", "[aout]",
                 "-c:a", "aac", str(project / "voice.m4a")])
            run([ffmpeg, "-y", "-i", str(silent_video), "-i", str(project / "voice.m4a"),
                 "-map", "0:v", "-map", "1:a",
                 "-vf", "subtitles=subtitles.srt:force_style='FontSize=22,Outline=2,Shadow=1'",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-c:a", "aac",
                 "-shortest", str(project / "final.mp4")], cwd=project)
        except subprocess.CalledProcessError:
            print("Audio mux/subtitle burn-in failed; saving video-only output.")
            shutil.copy2(silent_video, project / "final.mp4")
    else:
        run([ffmpeg, "-y", "-i", str(silent_video), "-vf", "subtitles=subtitles.srt",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-an",
             str(project / "final.mp4")], cwd=project)
    print(f"Done. Output: {project / 'final.mp4'}")
    print(f"Scenes: {len(scenes)} | Duration estimate: {sum(durations):.1f}s")
    if not any(voice_files):
        print("No local TTS voice was generated. Install espeak-ng with a Hindi voice or rerun with --no-voice.")


def main():
    parser = argparse.ArgumentParser(description="Create a local cinematic story preview without paid APIs.")
    parser.add_argument("story", help="UTF-8 .txt story file")
    parser.add_argument("--title", default="CineKatha Story")
    parser.add_argument("--output", default="output/cinekatha-project")
    parser.add_argument("--voice", default="hi", help="espeak-ng voice code (default: hi)")
    parser.add_argument("--rate", type=int, default=145)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--no-voice", action="store_true")
    args = parser.parse_args()
    try:
        build(args)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
