# CineKatha-AI

**An open-source, modular AI cinematic storytelling and film-production engine.**

CineKatha-AI turns a story, outline, or eligible public-domain literary work into a scene-by-scene cinematic video. The planned pipeline combines story direction, screenplay and shot planning, consistent characters, expressive narration, music, subtitles, and FFmpeg rendering.

> **Project status:** Early scaffold / architecture phase. The repository currently contains planning documents and a starter directory structure. Production features are not implemented yet.

## Vision

Create a cloud-first production workspace that can:
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
Web Dashboard
    -> Backend API
    -> Story Orchestrator
    -> Source & Rights Review
    -> Story Director
    -> Scene / Shot Planner
    -> Character + Emotion Direction
    -> Image / Voice / Music Providers
    -> Subtitle Engine
    -> FFmpeg Renderer
    -> Review, Export & Download
```

## Planned technology

| Layer | Initial direction |
|---|---|
| Web dashboard | Next.js |
| API | Python + FastAPI |
| Database | PostgreSQL |
| Background jobs | Redis + Celery |
| Object storage | S3-compatible storage |
| Story / planning models | Provider adapters for LLMs |
| Voice | Piper (local) and optional ElevenLabs integration |
| Visual assets | Openverse / Wikimedia Commons where licensing permits; pluggable image generation |
| Video rendering | FFmpeg |
| Deployment | Docker |
| CI | GitHub Actions |

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

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [ROADMAP.md](docs/ROADMAP.md).

## Getting started

This is a scaffold-only release. Runtime setup instructions will be added when the first backend and frontend milestones are implemented. Do not expect `docker compose up` to launch a working application yet.

## Cost strategy

The product is designed for a hybrid model:
- Prefer local or free/open-source tools for development and baseline processing.
- Make paid APIs optional, explicitly configured, and provider-swappable.
- Estimate costs before expensive generation jobs.
- Allow users to choose quality, speed, and cost profiles.
- Never silently call a paid provider.

## Copyright, licensing, and responsible use

Users are responsible for having the rights to submitted stories and assets. A work being old or published before 2000 does **not** automatically make it public domain. Verify the applicable jurisdiction, author death date, publication history, translations, editions, illustrations, recordings, and other derivative material. Prefer original, licensed, or verified public-domain sources. Preserve attribution and license information for sourced assets.

See [docs/COPYRIGHT_POLICY.md](docs/COPYRIGHT_POLICY.md) for the planned policy.

## Contributing

Contributions are welcome once implementation conventions are established. Please open an issue to discuss substantial changes before submitting a pull request. Keep provider integrations modular, document configuration, and add tests for new behavior.

## License

The repository license has not yet been selected. Until a license file is added, all rights are reserved by default; do not assume the code is licensed for reuse.
