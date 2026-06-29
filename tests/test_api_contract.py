import json

from conftest import AUTH_HEADERS, client

PNG_1X1_DATA_URL = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
)


def valid_request() -> dict:
    return {
        "model": "cpu-yolo-detector",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Detect objects."},
                    {"type": "image_url", "image_url": {"url": PNG_1X1_DATA_URL}},
                ],
            }
        ],
    }


def test_healthz_is_public() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_models_requires_auth() -> None:
    response = client.get("/v1/models")

    assert response.status_code == 401


def test_models_rejects_wrong_auth() -> None:
    response = client.get("/v1/models", headers={"Authorization": "Bearer wrong"})

    assert response.status_code == 401


def test_models_accepts_valid_auth() -> None:
    response = client.get("/v1/models", headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == "cpu-yolo-detector"


def test_chat_completion_accepts_single_base64_image() -> None:
    response = client.post("/v1/chat/completions", headers=AUTH_HEADERS, json=valid_request())

    assert response.status_code == 200

    body = response.json()
    assert body["object"] == "chat.completion"

    content = body["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    assert "detections" in parsed
    assert "track_id" not in content
    assert "mask" not in content
    assert "polygon" not in content
    assert "job_id" not in content
