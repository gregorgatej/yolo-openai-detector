# ADR 0005 — No background jobs in MVP

Date: 2026-06-29

## Status

Accepted.

## Decision

The MVP processes one image synchronously inside the HTTP request-response cycle.

## Rejected

- Celery;
- RQ;
- Redis job queue;
- `/jobs`;
- `/status`;
- polling;
- async completion webhooks.

## Rationale

Single-image detection should be simple enough for synchronous processing. Background jobs would create unnecessary complexity and encourage video/batch scope creep.

## Consequences

Requests must have reasonable image size limits and server timeouts.

If later inference becomes too slow, that is a separate product decision, not an automatic reason to add queues.
