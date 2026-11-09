# CineKatha-AI Roadmap

This roadmap is staged. A milestone is complete only when its acceptance criteria are met and documented.

## Phase 0 — Repository foundation
- [x] Create public repository and initial documentation.
- [x] Define proposed architecture and modular project layout.
- [ ] Select repository license after confirming dependency and contribution strategy.
- [ ] Add contribution guide and code of conduct.

**Exit criteria:** contributors can understand the project scope, architecture, rights principles, and next steps.

## Phase 1 — Backend foundation
- [ ] FastAPI application skeleton and health endpoint.
- [ ] PostgreSQL schema and migration tooling.
- [ ] Project/source CRUD and validation.
- [ ] Authentication and project-level authorization.
- [ ] Docker Compose development environment.
- [ ] Structured logging and configuration validation.

**Exit criteria:** create a project and persist source metadata locally.

## Phase 2 — Story director
- [ ] LLM provider interface and mock provider.
- [ ] Story ingestion and normalization.
- [ ] Story bible and character extraction.
- [ ] Outline, screenplay, scene, and shot schemas.
- [ ] Human review/edit checkpoints.
- [ ] Narrative and continuity validation tests.

**Exit criteria:** a text story becomes an editable, structured scene plan.

## Phase 3 — Rights and provenance
- [ ] Source provenance fields and evidence attachments.
- [ ] Public-domain/licensing review workflow.
- [ ] Asset license and attribution metadata.
- [ ] Warnings for uncertain or derivative rights.
- [ ] Exportable source/asset credits report.

**Exit criteria:** no source or external asset is treated as cleared merely because it is old or freely accessible.

## Phase 4 — Voice and emotion
- [ ] Voice provider interface and deterministic mock.
- [ ] Local Piper adapter.
- [ ] Optional hosted voice adapter.
- [ ] Speaker assignment, pronunciation dictionary, and emotion/delivery direction.
- [ ] Audio timing metadata and preview workflow.

**Exit criteria:** approved dialogue can be rendered into speaker-separated audio with timing metadata.

## Phase 5 — Visual generation and continuity
- [ ] Image provider interface.
- [ ] Licensed asset search adapter.
- [ ] Optional image generation adapter.
- [ ] Character reference sheet workflow.
- [ ] Style/location/prop continuity checks.
- [ ] Scene image review and regeneration.

**Exit criteria:** each approved scene has reviewed visual assets with provenance.

## Phase 6 — Music, subtitles, and rendering
- [ ] Music/sound provider interface and rights metadata.
- [ ] Subtitle generation (SRT/VTT).
- [ ] Timeline manifest format.
- [ ] FFmpeg renderer and configurable 16:9 1080p profile.
- [ ] Audio mixing, transitions, and output validation.
- [ ] Render retry/cancel and progress reporting.

**Exit criteria:** a reviewed scene package renders to a playable video with synchronized audio and subtitles.

## Phase 7 — Dashboard and cloud deployment
- [ ] Next.js project dashboard.
- [ ] Scene-by-scene editor and approval controls.
- [ ] Job progress, logs, and cost estimate display.
- [ ] S3-compatible asset storage.
- [ ] Deployment documentation, backups, monitoring, and CI.
- [ ] End-to-end tests and security review.

**Exit criteria:** a user can manage a project from source input through final export in a deployed environment.

## Guiding priorities

1. Build a reliable text-to-scene pipeline before attempting full video automation.
2. Use mock providers first so tests do not require paid APIs.
3. Keep every external provider replaceable.
4. Make cost and rights status visible before generation.
5. Preserve intermediate assets so failed jobs do not waste completed work.
