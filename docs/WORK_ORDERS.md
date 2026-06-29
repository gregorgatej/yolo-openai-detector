# Work Orders

This file stores initial recommended work orders for coding agents.

## Branch and PR rule

After the one-time repository bootstrap commit, all future work orders must use a named branch and open a pull request.

Direct commits or pushes to `main` are forbidden unless the human explicitly approves an exception in the current session.

Every future work order must state:

- Branch name
- Whether a PR is required
- Whether merging is forbidden

## Work Order 001 — Initial contract verification

### Goal

Install the repository, run the existing tests, and report whether the initial skeleton passes.

### Non-goals

- Do not add YOLO inference.
- Do not change the API contract.
- Do not add dependencies unless required to make the declared project install work.

### Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### Report

Use the final report format from `AGENTS.md`.

## Work Order 002 — Improve OpenAI-compatible error envelope

### Goal

Review the existing error responses and make them more consistently OpenAI-like without changing the accepted input contract.

### Non-goals

- No YOLO inference.
- No streaming.
- No URL fetching.
- No background jobs.

### Required tests

- missing auth;
- wrong auth;
- missing image;
- multiple images;
- URL image;
- invalid base64;
- stream rejected.

## Work Order 003 — Add ONNX Runtime CPU detector interface

### Goal

Introduce a real detector implementation boundary for ONNX Runtime CPU inference while preserving the existing mocked detector as a fallback for tests.

### Non-goals

- Do not commit a large model file.
- Do not add GPU dependencies.
- Do not add segmentation/tracking.
- Do not change public API shape.

### Requirements

- Use `onnxruntime`, not `onnxruntime-gpu`.
- Configure `providers=["CPUExecutionProvider"]`.
- Add tests that inspect configured providers.
- Document expected model location.

## Work Order 004 — Add YOLO preprocessing and postprocessing

### Goal

Implement preprocessing and postprocessing for the selected YOLO ONNX model.

### Non-goals

- No model training.
- No video.
- No batch processing.
- No tracking IDs.
- No masks.

### Requirements

- Document input size.
- Document class labels.
- Keep output schema stable.
- Add fixture tests.

## Work Order 005 — Add single-image benchmark

### Goal

Add a benchmark script for one local image and one local ONNX model.

### Non-goals

- No load testing.
- No server autoscaling.
- No background workers.

### Required output

The script prints CPU/system info and latency breakdown.
