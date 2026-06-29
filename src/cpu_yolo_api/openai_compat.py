import json
import time
import uuid

from cpu_yolo_api.config import settings
from cpu_yolo_api.detector import detector
from cpu_yolo_api.image_input import extract_single_base64_image
from cpu_yolo_api.schemas import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
)


def create_chat_completion(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """Process one OpenAI-style chat completion request."""

    if request.stream:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": "Streaming is not supported.",
                    "type": "invalid_request_error",
                    "code": "stream_not_supported",
                }
            },
        )

    image = extract_single_base64_image(request)
    detection_payload = detector.detect(image)

    content = json.dumps(
        detection_payload.model_dump(by_alias=True),
        separators=(",", ":"),
    )

    return ChatCompletionResponse(
        id=f"chatcmpl-local-{uuid.uuid4().hex}",
        created=int(time.time()),
        model=settings.model_name,
        choices=[
            ChatCompletionChoice(
                index=0,
                message={
                    "role": "assistant",
                    "content": content,
                },
            )
        ],
    )
