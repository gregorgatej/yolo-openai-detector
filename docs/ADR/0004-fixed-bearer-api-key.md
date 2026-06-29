# ADR 0004 — Fixed bearer API key

Date: 2026-06-29

## Status

Accepted for MVP.

## Decision

Use one fixed API key loaded from `YOLO_API_KEY`.

Clients authenticate with:

```http
Authorization: Bearer <YOLO_API_KEY>
```

## Rationale

The MVP is a simple service, probably single-tenant or controlled by an outer deployment boundary. A fixed key is enough for the initial version and mirrors the common OpenAI client authentication shape.

## Consequences

This is not full user management.

Future production versions may need:

- multiple keys;
- key rotation;
- scoped keys;
- request logging without secrets;
- rate limiting.
