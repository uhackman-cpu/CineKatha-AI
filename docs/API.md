# API Plan

**Status:** Planned; no production API is implemented yet.

The initial API will be versioned under `/api/v1`.

## Planned resource groups

| Resource | Planned operations |
|---|---|
| Projects | Create, list, retrieve, update, archive |
| Sources | Upload/register source, inspect provenance and rights status |
| Stories | Create and version story bible / screenplay |
| Scenes | List, inspect, edit, reorder, approve |
| Characters | Manage canonical descriptions and reference assets |
| Assets | List metadata, request signed upload/download URLs |
| Jobs | Submit, inspect status/progress, cancel |
| Renders | Create render from approved timeline, inspect/export result |

## Planned job endpoints

- `POST /api/v1/projects/{project_id}/jobs/story`
- `POST /api/v1/projects/{project_id}/jobs/voice`
- `POST /api/v1/projects/{project_id}/jobs/visuals`
- `POST /api/v1/projects/{project_id}/renders`
- `GET /api/v1/jobs/{job_id}`
- `POST /api/v1/jobs/{job_id}/cancel`

These are design placeholders and may change during implementation.

## API conventions

- JSON request/response bodies.
- Explicit schema validation.
- Authenticated, project-scoped access.
- Stable error codes and request IDs.
- Pagination for collection endpoints.
- Idempotency keys for expensive job submission.
- Provider cost estimate and confirmation before paid work.
- No provider secrets in client responses.

OpenAPI documentation will be generated from FastAPI once the service exists.
