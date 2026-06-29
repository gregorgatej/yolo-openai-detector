#!/usr/bin/env bash
set -euo pipefail

export YOLO_API_KEY="${YOLO_API_KEY:-dev-secret-change-me}"
uvicorn cpu_yolo_api.main:app --reload
