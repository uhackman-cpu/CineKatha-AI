# Local MVP — Story to Cinematic Preview

This prototype creates storyboard frames, Hindi/English neural narration, SRT subtitles, and an MP4.

## Requirements

- Python 3.10+
- FFmpeg and FFprobe on PATH
- Python dependencies: `python -m pip install -r requirements.txt`
- Internet access for Microsoft Edge Neural TTS (free to use, no API key/account in this project)
- Optional: `espeak-ng` for the explicitly selected robotic offline fallback

## Run (natural neural narration by default)

From the repository root:

```bash
cd backend
python -m pip install -r requirements.txt
python cinekatha.py sample_story_hi.txt --title "आरव और नीला तारा" --output ../output/arav-preview
```

Default Hindi voice: `hi-IN-SwaraNeural` (female). Choose a male voice with:

```bash
python cinekatha.py sample_story_hi.txt --voice-gender male --output ../output/arav-male
```

English narration:

```bash
python cinekatha.py sample_story_hi.txt --language en --output ../output/arav-english
```

## Voice modes

- `--tts-engine edge` — default; natural neural voices through Edge TTS. Requires internet.
- `--tts-engine espeak` — optional offline fallback; robotic sound is expected.
- `--no-voice` — render without narration.

The renderer creates one narration clip per scene, measures each clip with FFprobe, and aligns scene timing and subtitles to the actual generated speech. If Edge TTS fails, the build stops with an error instead of silently replacing the requested neural voice with robotic eSpeak audio.

The Edge TTS service is a free online dependency, not an unlimited or guaranteed service. No paid API key or subscription is used.

## Current limitations

- This MVP converts story paragraphs/sentences into scenes; it does not yet perform web research or use a language model to write a screenplay.
- Frames are typographic storyboard cards, not generated photorealistic images.
- Neural narration requires an internet connection.
- Long stories can create large output files; start with a short sample.
- Always use stories and audio/visual assets you own or have permission to use.
