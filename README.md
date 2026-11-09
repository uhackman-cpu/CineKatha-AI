# CineKatha-AI

**An open-source, modular AI cinematic storytelling and film-production engine.**

CineKatha-AI turns a story, outline, or eligible public-domain literary work into a scene-by-scene cinematic video. The planned pipeline combines story direction, screenplay and shot planning, consistent characters, expressive narration, music, subtitles, and FFmpeg rendering.

> **Project status:** First local MVP added. The backend can split a UTF-8 story into scenes, create 1080p typographic storyboard frames, generate optional local speech with espeak-ng/espeak, write SRT subtitles, and render an MP4 with FFmpeg. It is an early storyboard-video prototype, not a photorealistic AI video generator.

## Vision

Create a production workspace that can:
- Accept an original story, outline, or properly licensed/public-domain source.
- Break the narrative into scenes, shots, dialogue, and visual directions.
- Maintain character descriptions and continuity across scenes.
- Generate or source visuals through interchangeable providers.
- Produce expressive voice performances with emotion and delivery direction.
- Add licensed music, sound design, and synchronized subtitles.
- Render a long-form 16:9 video, targeting 1080p output.
- Export project assets and a final video.

## Planned pipeline

```text
Dashboard / Local UI
    -> Story Research & Rights Review
    -> Story Director
    -> Screenplay + Scene / Shot Planner
    -> Character + Emotion Direction
    -> Visual / Voice / Music Assets
    -> Subtitle Engine
    -> FFmpeg Renderer
    -> Quality Review & Export
```

## Planned technology

| Layer | Initial direction |
|---|---|
| Web dashboard | Next.js (when needed) |
| API | Python + FastAPI |
| Database | SQLite for first local MVP; PostgreSQL when needed |
| Background jobs | Local Python worker first |
| Voice | Piper or another locally runnable open-source TTS |
| Visual assets | Original assets; Openverse / Wikimedia Commons only where license permits |
| Video rendering | FFmpeg |
| Deployment | Local-first; optional free hosting only if its current limits fit |
| CI | GitHub Actions within available free limits |

These are architectural choices, not claims that the integrations are already implemented. Providers will be replaceable through stable interfaces.

## Repository layout

- `frontend/` — dashboard and project UI
- `backend/` — API, authentication, persistence, and workers
- `engine/` — story, scene, character, emotion, media, subtitle, and rendering orchestration
- `providers/` — adapters for LLM, image, voice, and storage services
- `templates/` — reusable genre and production templates
- `tests/` — automated tests
- `docs/` — architecture, roadmap, API, and rights policy
- `.github/workflows/` — CI automation

See [ARCHITECTURE.md](docs/ARCHITECTURE.md), [ROADMAP.md](docs/ROADMAP.md), and [FREE_BUDGET_STRATEGY.md](docs/FREE_BUDGET_STRATEGY.md).

## Getting started — local MVP

The first prototype runs locally and does not require API keys or hosted services. See [backend/README.md](backend/README.md) for requirements and commands. In short:

```bash
cd backend
python -m pip install -r requirements.txt
python cinekatha.py sample_story_hi.txt --title "आरव और नीला तारा" --output ../output/arav-preview
```

FFmpeg is required for MP4 output. `espeak-ng`/`espeak` with a Hindi voice is optional for narration. The current visuals are cinematic storyboard cards; photorealistic image generation and AI research are not implemented yet.

## ₹0 budget commitment

**The default project must not require paid APIs, subscriptions, cloud GPUs, paid hosting, paid storage, or purchased credits.** The first working version will be local-first and use free/open-source software wherever practical. Paid services, if ever documented, will be optional, disabled by default, and never called without explicit user approval.

Free hosted tiers can have quotas, sleep limits, expiry, or changing terms; we will not describe them as unlimited or guaranteed. High-end AI video generation may not be achievable at unlimited length or quality for free. If a feature cannot be delivered within ₹0, we will disclose that and use the best practical free alternative rather than incur a charge.

See [docs/FREE_BUDGET_STRATEGY.md](docs/FREE_BUDGET_STRATEGY.md).

## Research and production workflow

The assistant will help research topics, check factual claims against sources, develop the story, write the screenplay, plan scenes and shots, prepare visual/voice/music directions, create subtitles, and review production outputs. Actual rendering and large model inference still require an available execution environment and compute; a render will only be marked complete after a real output file is produced and checked.

## Copyright, licensing, and responsible use

Users must have rights to submitted stories and assets. A work being old or published before 2000 does **not** automatically make it public domain. Verify the applicable jurisdiction, author death date, publication history, translations, editions, illustrations, recordings, and derivative material. Preserve source URLs, creator, license, attribution, access date, and modifications for every third-party asset.

See [docs/COPYRIGHT_POLICY.md](docs/COPYRIGHT_POLICY.md).

## Contributing

Contributions are welcome once implementation conventions are established. Please open an issue to discuss substantial changes before submitting a pull request. Keep provider integrations modular, document configuration, and add tests for new behavior.

## License

The repository license has not yet been selected. Until a license file is added, all rights are reserved by default; do not assume the code is licensed for reuse.
