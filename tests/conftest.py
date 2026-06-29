import os

os.environ.setdefault("YOLO_API_KEY", "test-key")
os.environ.setdefault("YOLO_MODEL_NAME", "cpu-yolo-detector")

from fastapi.testclient import TestClient  # noqa: E402

from cpu_yolo_api.main import app  # noqa: E402

client = TestClient(app)
AUTH_HEADERS = {"Authorization": "Bearer test-key"}
