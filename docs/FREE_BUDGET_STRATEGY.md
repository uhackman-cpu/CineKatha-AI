# ₹0 Budget Strategy

CineKatha-AI is designed to have **zero mandatory monetary cost**. Paid providers are not part of the default path and must never be silently enabled.

## Non-negotiable rules

1. No paid API, subscription, cloud GPU, domain, storage bucket, or credits are required for the core workflow.
2. No card details or billing account should be required to run the baseline project.
3. Prefer open-source software and user-controlled local processing.
4. Optional external services must be clearly marked, disabled by default, and show their possible cost before use.
5. Never describe a limited free tier as unlimited or guaranteed. Provider quotas and terms can change.
6. If a feature cannot be delivered at acceptable quality for ₹0, disclose the limitation and offer a lower-cost-free alternative rather than activating a paid service.

## Default free stack

| Need | Default choice | Notes |
|---|---|---|
| Source code and collaboration | GitHub | Public repository; GitHub service limits apply |
| Backend | Python + FastAPI | Open-source |
| Database | SQLite for first local MVP; PostgreSQL when needed | Avoids requiring a hosted database |
| Background jobs | Python process / local queue first | Redis is optional for later scaling |
| Story research and writing | Human-reviewed research workflow with source links | Verify facts, dates, and rights |
| Text-to-speech | Piper or another locally runnable open-source TTS | Voice quality and language coverage vary |
| Images | Original generated assets where available; Openverse/Wikimedia Commons only after checking each asset's license | Attribution and usage restrictions must be preserved |
| Editing and rendering | FFmpeg | Open-source; rendering uses local CPU/GPU and storage |
| Subtitles | Generated SRT/VTT using local tools | Review timing and spelling |
| Deployment | Local run first; free hosting only if a currently available free tier fits | Free tiers may sleep, expire, or impose quotas |

## First zero-cost milestone

The first usable version should run locally and produce a short sample video from:
- a user-provided story or a source whose rights have been checked;
- a scene-by-scene script and shot list;
- still images or legally reusable visual assets;
- locally generated narration where supported;
- subtitles, music/sound effects with verified rights, and FFmpeg assembly.

This is a practical first milestone. It is not a promise of unlimited photorealistic AI video generation: high-end video models commonly require substantial compute, and free access may be limited or unavailable.

## Free-tier and copyright safeguards

- Check current terms, quotas, attribution, commercial-use permissions, and geographic restrictions before integrating any hosted free service.
- Do not scrape or reuse copyrighted films, clips, music, voices, or artwork without permission.
- A work being old or published before 2000 does not automatically make it public domain.
- Record source URL, creator, license, access date, attribution text, and modifications for every third-party asset.
- Never upload private user stories or credentials to third-party services without explicit consent.

## Honest capability boundary

The assistant can research topics, verify and cite sources, develop the story, write the screenplay, design scenes and shots, prepare image/voice/music prompts, create subtitles, review outputs, and help build the rendering pipeline. Actual video rendering and large AI model inference require an available execution environment and compute. This repository must not claim a video has been rendered unless a real output file has been produced and checked.
