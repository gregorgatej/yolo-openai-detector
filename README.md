# CPU YOLO OpenAI-Compatible Image Detection API

A CPU-only, single-image YOLO object detection service with an OpenAI-compatible HTTP surface.

This repository is initialized as a **contract-first project**. The first version is intentionally small: it accepts exactly one base64 image in an OpenAI-style `/v1/chat/completions` request and returns object detections as JSON inside an OpenAI-like chat completion response.

## Product scope

The service is for **single-shot object detection on one image**.

It is not a tracking system. It is not a segmentation system. It is not a video service. It is not a background-job service.

## MVP behavior

The MVP must:

- run on a GPU-less machine;
- expose an OpenAI-compatible `/v1/chat/completions` endpoint;
- accept exactly one image encoded as a base64 data URL;
- require a fixed bearer API key;
- synchronously return detection results;
- return bounding boxes, class names, and confidence scores;
- avoid all GPU-only dependencies.

## Non-goals

The following are intentionally out of scope:

- no object tracking;
- no video processing;
- no segmentation;
- no masks;
- no pose estimation;
- no OCR;
- no background jobs;
- no queues;
- no polling endpoints;
- no job IDs;
- no batch image processing in the MVP;
- no remote image URL fetching in the MVP;
- no CUDA;
- no TensorRT;
- no `onnxruntime-gpu`;
- no user accounts;
- no dynamic API key management;
- no billing;
- no production deployment automation in the initial slice.

## API overview

### Health

```http
GET /healthz
```

This endpoint is intentionally unauthenticated.

### Models

```http
GET /v1/models
Authorization: Bearer <YOLO_API_KEY>
```

Returns an OpenAI-like model list.

### Chat completions

```http
POST /v1/chat/completions
Authorization: Bearer <YOLO_API_KEY>
Content-Type: application/json
```

Example request:

```json
{
  "model": "cpu-yolo-detector",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Detect objects in this image."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
          }
        }
      ]
    }
  ]
}
```

Example response shape:

```json
{
  "id": "chatcmpl-local-...",
  "object": "chat.completion",
  "created": 1782730000,
  "model": "cpu-yolo-detector",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\"detections\":[{\"class\":\"mock_object\",\"confidence\":0.99,\"box\":{\"x1\":0,\"y1\":0,\"x2\":1,\"y2\":1}}]}"
      },
      "finish_reason": "stop"
    }
  ]
}
```

The initial skeleton returns mocked detections. Real CPU YOLO inference is a later bounded implementation slice.

## Input contract

The API accepts exactly one image.

Allowed:

- `data:image/jpeg;base64,...`
- `data:image/png;base64,...`

Rejected:

- missing image;
- multiple images;
- `http://...` image URLs;
- `https://...` image URLs;
- video files;
- invalid base64;
- unsupported media types;
- images over the configured size limit.

## Environment variables

Copy `.env.example` to `.env` for local development.

```bash
YOLO_API_KEY=dev-secret-change-me
YOLO_MODEL_NAME=cpu-yolo-detector
YOLO_MAX_IMAGE_BYTES=10485760
```

Do not commit real secrets.

## Local development

Create a virtual environment and install the project with development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the API:

```bash
YOLO_API_KEY=dev-secret-change-me uvicorn cpu_yolo_api.main:app --reload
```

Try the health endpoint:

```bash
curl http://127.0.0.1:8000/healthz
```

Try the model list:

```bash
curl \
  -H "Authorization: Bearer dev-secret-change-me" \
  http://127.0.0.1:8000/v1/models
```

## Architecture decisions

See:

- `docs/ARCHITECTURE.md`
- `docs/API_CONTRACT.md`
- `docs/SECURITY.md`
- `docs/VALIDATION.md`
- `docs/ADR/`

## Agent governance

Agents must follow:

- `AGENTS.md`
- `CLAUDE.md`

`CLAUDE.md` is intentionally equivalent to `AGENTS.md` and exists so Claude Code sees the same project constitution as Codex-style agents.

## External references

These links are included to anchor future implementation work:

- OpenAI Chat Completions API: https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/
- FastAPI security tutorial: https://fastapi.tiangolo.com/tutorial/security/first-steps/
- ONNX Runtime execution providers: https://onnxruntime.ai/docs/execution-providers/
- ONNX Runtime Python getting started: https://onnxruntime.ai/docs/get-started/with-python.html
- Ultralytics YOLO object detection task: https://docs.ultralytics.com/tasks/detect/
