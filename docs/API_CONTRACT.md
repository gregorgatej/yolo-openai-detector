# API Contract

## Compatibility goal

The service exposes a minimal OpenAI-compatible surface, not a full OpenAI clone.

Supported endpoints:

- `GET /healthz`
- `GET /v1/models`
- `POST /v1/chat/completions`

Unsupported OpenAI capabilities:

- streaming;
- tools/function calling;
- Responses API;
- Assistants API;
- embeddings;
- image generation;
- file uploads;
- fine tuning.

## Authentication

All `/v1/*` endpoints require:

```http
Authorization: Bearer <YOLO_API_KEY>
```

`/healthz` is public.

## `GET /v1/models`

Example response:

```json
{
  "object": "list",
  "data": [
    {
      "id": "cpu-yolo-detector",
      "object": "model",
      "created": 0,
      "owned_by": "local"
    }
  ]
}
```

## `POST /v1/chat/completions`

### Request

Required fields:

- `model`
- `messages`

The request must contain exactly one image part.

Example:

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
            "url": "data:image/png;base64,..."
          }
        }
      ]
    }
  ]
}
```

### Allowed image inputs

Allowed:

- `data:image/jpeg;base64,...`
- `data:image/jpg;base64,...`
- `data:image/png;base64,...`

Rejected:

- missing image;
- more than one image;
- `http://...`;
- `https://...`;
- unsupported media types;
- invalid base64;
- images above size limit.

### Response

The response is an OpenAI-like chat completion. The detection payload is serialized as JSON inside `choices[0].message.content`.

Example:

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
        "content": "{\"detections\":[{\"class\":\"person\",\"confidence\":0.91,\"box\":{\"x1\":120,\"y1\":80,\"x2\":420,\"y2\":700}}]}"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

### Detection payload schema

Inside `message.content`:

```json
{
  "detections": [
    {
      "class": "person",
      "confidence": 0.91,
      "box": {
        "x1": 120,
        "y1": 80,
        "x2": 420,
        "y2": 700
      }
    }
  ],
  "image": {
    "width": 640,
    "height": 480,
    "media_type": "image/png"
  },
  "metadata": {
    "engine": "mock",
    "cpu_only": true,
    "tracking": false,
    "segmentation": false
  }
}
```

Forbidden fields:

- `track_id`;
- `mask`;
- `polygon`;
- `job_id`.

## Error shape

Use OpenAI-like error objects where practical:

```json
{
  "detail": {
    "error": {
      "message": "Exactly one image is allowed per request.",
      "type": "invalid_request_error",
      "code": "multiple_images"
    }
  }
}
```

## Current limitations

The initial skeleton returns mock detections. Real YOLO inference is intentionally a later implementation slice.
