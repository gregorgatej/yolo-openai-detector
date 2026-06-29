from conftest import AUTH_HEADERS, client

PNG_1X1_DATA_URL = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
)


def post(payload: dict):
    return client.post("/v1/chat/completions", headers=AUTH_HEADERS, json=payload)


def test_missing_image_returns_400() -> None:
    response = post({
        "model": "cpu-yolo-detector",
        "messages": [{"role": "user", "content": "Detect objects."}],
    })

    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "missing_image"


def test_multiple_images_return_400() -> None:
    response = post({
        "model": "cpu-yolo-detector",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": PNG_1X1_DATA_URL}},
                    {"type": "image_url", "image_url": {"url": PNG_1X1_DATA_URL}},
                ],
            }
        ],
    })

    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "multiple_images"


def test_remote_url_is_rejected() -> None:
    response = post({
        "model": "cpu-yolo-detector",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
                ],
            }
        ],
    })

    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "remote_url_not_supported"


def test_invalid_base64_is_rejected() -> None:
    response = post({
        "model": "cpu-yolo-detector",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64,not-valid"}},
                ],
            }
        ],
    })

    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "invalid_base64"


def test_streaming_is_rejected() -> None:
    response = post({
        "model": "cpu-yolo-detector",
        "stream": True,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": PNG_1X1_DATA_URL}},
                ],
            }
        ],
    })

    assert response.status_code == 400
    assert response.json()["detail"]["error"]["code"] == "stream_not_supported"
