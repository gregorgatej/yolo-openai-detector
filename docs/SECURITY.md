# Security

## Authentication model

The MVP uses one fixed bearer API key loaded from the environment variable:

```bash
YOLO_API_KEY=...
```

All `/v1/*` endpoints require:

```http
Authorization: Bearer <YOLO_API_KEY>
```

`/healthz` is unauthenticated.

## Secret handling

Rules:

- never commit `.env`;
- never commit real API keys;
- never log the bearer token;
- never return the bearer token in errors;
- use fake secrets in tests;
- keep production secrets out of agent environments.

## Request validation

The service must reject:

- remote image URLs;
- missing images;
- multiple images;
- invalid base64;
- unsupported image types;
- oversized images.

## Why remote image URLs are excluded

Remote URL fetching creates unnecessary MVP risk:

- SSRF;
- internal network probing;
- unclear timeout behavior;
- redirects;
- credential leakage through outbound requests;
- oversized downloads;
- content-type ambiguity.

The MVP avoids this by accepting only base64 data URLs.

## Error handling

Client-visible errors must not leak:

- local file paths;
- stack traces;
- environment variables;
- model file locations;
- installed package details;
- API keys.

## Dependency risk

Forbidden unless explicitly approved:

- `onnxruntime-gpu`;
- CUDA packages;
- TensorRT;
- unnecessary cloud SDKs;
- database clients;
- background-job systems.

## Agent safety

Coding agents must not:

- add production credentials;
- call real third-party APIs during tests;
- download unknown binaries without documenting the source;
- commit model artifacts;
- introduce network image fetching;
- weaken authentication.
