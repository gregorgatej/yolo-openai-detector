"""Placeholder for future single-image CPU benchmark.

This script is intentionally not implemented yet because the initial repository
uses a mocked detector. A future work order should add ONNX Runtime CPU inference
first, then implement this benchmark against a real local ONNX model.
"""

from __future__ import annotations


def main() -> None:
    raise SystemExit(
        "Benchmark is not implemented yet. Add real CPU ONNX inference first."
    )


if __name__ == "__main__":
    main()
