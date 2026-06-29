# Roadmap

## Phase 0 — Repository initialization

Status: initialized by this package.

Deliverables:

- project constitution;
- README;
- API contract;
- security policy;
- validation plan;
- ADRs;
- runnable mocked FastAPI skeleton;
- initial tests.

## Phase 1 — Contract-complete mock service

Goal:

- ensure the API/auth/image validation contract works before adding YOLO.

Acceptance:

- all current tests pass;
- README examples are accurate;
- no real inference claims are made.

## Phase 2 — CPU ONNX inference boundary

Goal:

- add ONNX Runtime CPU inference interface.

Acceptance:

- CPU provider explicitly configured;
- no GPU package/dependency;
- model load failure handled cleanly;
- mocked detector remains usable for contract tests.

## Phase 3 — Real YOLO model integration

Goal:

- run YOLO object detection on one image.

Acceptance:

- valid detection payload from fixture image;
- bounding boxes, labels, confidences only;
- no masks;
- no track IDs.

## Phase 4 — Benchmark and deployment notes

Goal:

- document expected performance on CPU-only machine.

Acceptance:

- benchmark script;
- example results;
- deployment runbook;
- resource limits.

## Explicitly postponed

- streaming;
- video;
- tracking;
- segmentation;
- background jobs;
- batch requests;
- remote URL image fetching;
- production-grade key management.
