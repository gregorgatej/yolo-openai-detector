# AGENTS.md — Project Constitution

This file is the authoritative instruction set for all coding agents working in this repository.

The project is a **CPU-only, single-image YOLO object detection API** with an OpenAI-compatible HTTP interface. Agents must preserve the product scope, non-goals, security model, and validation discipline defined here.

## 1. Mission

Build a service that:

1. runs on GPU-less machines;
2. accepts exactly one base64-encoded image through an OpenAI-style chat completion request;
3. performs object detection only;
4. returns bounding boxes, class labels, and confidence scores;
5. uses fixed bearer API key authentication;
6. responds synchronously;
7. is test-backed and reviewable.

## 2. Product identity

This is:

- an image object detection API;
- a CPU-first inference service;
- an OpenAI-compatible adapter surface;
- a synchronous request-response service;
- a contract-first implementation.

This is not:

- a tracking API;
- a video analytics platform;
- a segmentation service;
- a queue-based processing system;
- a general multimodal LLM;
- a full OpenAI API clone.

## 3. Hard constraints

Agents must not violate these constraints without explicit human approval.

### 3.1 CPU-only

The runtime must work on machines without GPUs.

Forbidden unless explicitly approved:

- CUDA;
- TensorRT;
- `onnxruntime-gpu`;
- GPU-only packages;
- code paths that require NVIDIA drivers;
- tests that pass only when a GPU is present.

When ONNX Runtime is introduced, use `CPUExecutionProvider` explicitly and test for CPU-only behavior.

### 3.2 Single image only

The MVP accepts exactly one image per request.

Forbidden:

- multiple image inputs;
- video inputs;
- frame sequences;
- zip files of images;
- streaming image input;
- batch processing.

### 3.3 Detection only

The API returns object detections.

Allowed fields:

- class label;
- confidence;
- bounding box coordinates;
- optional model/version metadata.

Forbidden output fields:

- `track_id`;
- `mask`;
- `polygon`;
- segmentation masks;
- pose keypoints;
- job IDs.

### 3.4 No background jobs

The MVP is synchronous.

Forbidden:

- task queues;
- Celery;
- RQ;
- Redis as a job broker;
- background workers;
- `/jobs`;
- `/status`;
- polling endpoints;
- webhooks for completion.

### 3.5 Base64 image input only

The MVP accepts image data as a data URL in the OpenAI-style `image_url.url` field.

Allowed:

- `data:image/jpeg;base64,...`
- `data:image/png;base64,...`

Forbidden in MVP:

- `http://...`;
- `https://...`;
- filesystem paths;
- S3 URLs;
- multipart uploads;
- binary request bodies.

Remote URL fetching is intentionally excluded for SSRF/security simplicity.

### 3.6 Fixed bearer API key only

Authentication is a single fixed bearer key loaded from environment.

Use:

```http
Authorization: Bearer <YOLO_API_KEY>
```

Do not:

- commit API keys;
- log API keys;
- invent user accounts;
- add OAuth;
- add database-backed key management;
- add admin endpoints for key rotation.

## 4. API compatibility posture

The service is **OpenAI-compatible where useful**, not OpenAI-identical.

Required:

- `/v1/models`;
- `/v1/chat/completions`;
- bearer authorization;
- OpenAI-like response envelope;
- OpenAI-like error envelope where practical.

Not required:

- full OpenAI parameter support;
- streaming;
- tools/function calling;
- assistants;
- responses API;
- embeddings;
- images generation API;
- files API.

Unsupported OpenAI fields must either be safely ignored or rejected with clear errors. Prefer rejection when accepting the field would imply behavior the service does not implement.

## 5. Repository layout

Expected layout:

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── docs/
│   ├── API_CONTRACT.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── SECURITY.md
│   ├── VALIDATION.md
│   ├── WORK_ORDERS.md
│   └── ADR/
├── models/
├── scripts/
├── src/
│   └── cpu_yolo_api/
└── tests/
```

Do not move major folders without updating this file, README, and docs.

## 6. Coding standards

Use:

- Python 3.11 or newer;
- FastAPI for the HTTP service;
- Pydantic for request/response models;
- pytest for tests;
- explicit type hints for public functions;
- small modules with clear responsibilities.

Avoid:

- large framework abstractions;
- hidden global state;
- unnecessary dependency injection frameworks;
- premature database introduction;
- background service infrastructure;
- configuration spread across many files.

## 7. Dependency policy

Initial runtime dependencies should stay boring and minimal.

Allowed baseline dependencies:

- `fastapi`;
- `uvicorn`;
- `pydantic`;
- `pydantic-settings`;
- `pillow`;
- `numpy`;
- `onnxruntime` when real inference is introduced.

Allowed development dependencies:

- `pytest`;
- `httpx`;
- `ruff`;
- `mypy` if useful.

Do not add large dependencies without explaining why. Never add `onnxruntime-gpu`.

## 8. Model artifact policy

Do not commit large model artifacts to Git.

Use the `models/` directory as a local placeholder only. It contains `.gitkeep` so the folder exists.

Future model handling must document:

- source model;
- export command;
- ONNX opset/version;
- expected input size;
- class labels;
- checksum;
- license constraints;
- how to reproduce the artifact.

## 9. Security requirements

Agents must preserve these rules:

- API key is loaded from environment.
- API key is compared safely.
- API key is not logged.
- Invalid or missing auth returns `401`.
- Image URLs from the network are rejected in MVP.
- Image size is limited.
- Image decoding failures are handled without stack traces to the client.
- Error responses do not leak local paths or secrets.
- `.env` is ignored by Git.
- Tests must not use real secrets.

See `docs/SECURITY.md`.

## 10. Validation requirements

Every implementation PR must include or update tests.

At minimum, the project must test:

- `/healthz` works;
- `/v1/models` requires auth;
- missing auth returns `401`;
- wrong bearer key returns `401`;
- valid single base64 image succeeds;
- missing image returns `400`;
- multiple images return `400`;
- URL image input returns `400`;
- invalid base64 returns `400`;
- response does not include tracking or segmentation fields.

When real inference is introduced, add tests proving:

- CPU provider only;
- no CUDA provider is configured;
- output schema remains stable;
- at least one fixture image produces valid detection JSON;
- confidence threshold handling is deterministic.

## 11. Definition of done

A task is not done until:

1. the code is scoped to the work order;
2. tests were added or updated;
3. relevant tests pass locally;
4. docs are updated if behavior changed;
5. no non-goal was introduced;
6. no GPU-only dependency was added;
7. no secret was committed;
8. the final report lists files changed, commands run, tests run, assumptions, and known gaps.

## 12. Work-order protocol

Agents must work from narrow work orders.

A valid work order includes:

- goal;
- non-goals;
- required files or areas;
- acceptance criteria;
- required tests;
- final report format.

Agents must not silently expand scope.

If the requested change conflicts with this constitution, stop and report the conflict.

## 13. Final report format

Every agent run must end with:

```markdown
## Summary
- ...

## Files changed
- ...

## Commands run
- ...

## Tests
- ...

## Contract checks
- CPU-only:
- single image only:
- no tracking:
- no segmentation:
- no background jobs:
- base64-only input:
- fixed bearer key:

## Assumptions
- ...

## Known gaps
- ...

## Recommended next work order
- ...
```

## 14. Human review checklist

Before accepting a change, the human or strategic agent should ask:

- Did this implement the exact work order?
- Did it introduce video, tracking, segmentation, jobs, queues, or GPU dependency?
- Are errors clean and non-leaky?
- Are tests meaningful or only superficial?
- Is the README still accurate?
- Are unsupported OpenAI parameters handled honestly?
- Can this still run on a GPU-less machine?

## 15. External references

Use official references where possible:

- OpenAI Chat Completions API: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/
- FastAPI security tutorial: https://fastapi.tiangolo.com/tutorial/security/first-steps/
- ONNX Runtime execution providers: https://onnxruntime.ai/docs/execution-providers/
- ONNX Runtime Python getting started: https://onnxruntime.ai/docs/get-started/with-python.html
- Ultralytics YOLO detect task: https://docs.ultralytics.com/tasks/detect/
