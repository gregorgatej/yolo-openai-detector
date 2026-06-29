# Architecture

## System purpose

The service exposes a small OpenAI-compatible API surface for CPU-only single-image object detection.

It is intentionally not a general computer vision platform.

## Logical architecture

```text
Client using OpenAI-style HTTP
        |
        | Authorization: Bearer <fixed key>
        v
FastAPI app
        |
        +-- /healthz
        +-- /v1/models
        +-- /v1/chat/completions
        |
        v
Request validator
        |
        +-- validates OpenAI-like chat request
        +-- extracts exactly one base64 data URL image
        +-- rejects URLs, videos, batches, invalid base64
        |
        v
Detector interface
        |
        +-- current: mock detector
        +-- future: ONNX Runtime CPU YOLO detector
        |
        v
OpenAI-like response formatter
```

## Runtime architecture

Initial runtime:

```text
Python 3.11+
FastAPI
Pydantic
Pillow image validation
Mock detector
pytest
```

Future inference runtime:

```text
Python 3.11+
FastAPI
Pydantic
Pillow / NumPy preprocessing
ONNX Runtime CPUExecutionProvider
YOLO ONNX model
```

## Trust boundaries

### Client boundary

Clients are untrusted.

The service must validate:

- authorization;
- request size;
- image count;
- media type;
- base64 validity;
- decoded image validity.

### Model boundary

The model artifact is local and trusted only after documented export/checksum review.

Large model files must not be committed.

### Network boundary

The MVP must not fetch remote images. This avoids SSRF, timeouts, remote content-type ambiguity, and credential-leaking fetches.

## Failure behavior

Use clear `400` errors for invalid requests.

Use `401` for missing or invalid API keys.

Do not leak:

- local file paths;
- environment variables;
- stack traces;
- model paths;
- API keys.

## Performance posture

The project is CPU-first, so performance must be measured and optimized deliberately.

Future benchmark dimensions:

- image resolution;
- model variant;
- preprocessing time;
- inference time;
- postprocessing time;
- total request latency;
- memory usage;
- CPU model and core/thread count.

## Future implementation sequence

1. Keep mocked detector and stabilize API contract.
2. Add real image preprocessing.
3. Add ONNX Runtime CPU detector.
4. Add deterministic fixture image tests.
5. Add benchmark script.
6. Add deployment docs.
