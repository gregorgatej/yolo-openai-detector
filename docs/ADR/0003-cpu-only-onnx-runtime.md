# ADR 0003 — CPU-only ONNX Runtime for inference

Date: 2026-06-29

## Status

Accepted for future inference slice.

## Decision

When real inference is added, use ONNX Runtime with the CPU execution provider.

Use the `onnxruntime` package, not `onnxruntime-gpu`.

Configure:

```python
providers = ["CPUExecutionProvider"]
```

## Rationale

The product must run on GPU-less machines. ONNX Runtime gives a practical CPU inference target and avoids requiring the full training framework at runtime.

## Consequences

Performance must be benchmarked on CPU.

The implementation must avoid CUDA/TensorRT assumptions.
