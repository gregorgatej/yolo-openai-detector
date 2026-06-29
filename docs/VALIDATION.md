# Validation Plan

## Core contract tests

The initial test suite must verify:

- `/healthz` works without auth;
- `/v1/models` requires bearer auth;
- missing bearer auth returns `401`;
- invalid bearer auth returns `401`;
- valid bearer auth succeeds;
- `/v1/chat/completions` accepts exactly one base64 image;
- missing image returns `400`;
- multiple images return `400`;
- remote URL image input returns `400`;
- invalid base64 returns `400`;
- streaming request returns `400`;
- response contains detections;
- response does not contain tracking or segmentation fields.

## Future real-inference tests

When real YOLO/ONNX inference is added, tests must verify:

- `onnxruntime` CPU package is used;
- `CPUExecutionProvider` is configured explicitly;
- no CUDA provider is configured;
- a fixture image returns deterministic schema;
- empty/no-object image behavior is documented;
- confidence threshold behavior is deterministic;
- model load errors are clean.

## Benchmark plan

Future `scripts/benchmark_single_image.py` should report:

- CPU model;
- OS;
- Python version;
- model file;
- image dimensions;
- preprocessing time;
- inference time;
- postprocessing time;
- total latency;
- peak memory if feasible.

## Validation debt rule

A feature without tests is not complete.

A performance claim without a benchmark command is not complete.

A CPU-only claim without a CPU-provider check is not complete.
