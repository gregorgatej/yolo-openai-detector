# ADR 0002 — Use OpenAI-compatible `/v1/chat/completions`

Date: 2026-06-29

## Status

Accepted.

## Decision

The service exposes `/v1/chat/completions` and `/v1/models`.

Images are passed through an OpenAI-style message content part:

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/png;base64,..."
  }
}
```

## Rationale

Many users and SDKs understand OpenAI-style bearer auth and `/v1/chat/completions` request/response envelopes. This lets the service behave like a local OpenAI-compatible provider while performing image detection instead of language generation.

## Consequences

The service is OpenAI-compatible where useful, but not OpenAI-identical. Unsupported fields such as streaming must be rejected or ignored honestly.
