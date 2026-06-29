from fastapi import Depends, FastAPI

from cpu_yolo_api.config import settings
from cpu_yolo_api.openai_compat import create_chat_completion
from cpu_yolo_api.schemas import ChatCompletionRequest, ChatCompletionResponse
from cpu_yolo_api.security import require_api_key

app = FastAPI(
    title="CPU YOLO OpenAI-Compatible Image Detection API",
    version="0.1.0",
    description="CPU-only single-image object detection API with an OpenAI-compatible surface.",
)


@app.get("/healthz")
def healthz() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "cpu-yolo-openai-api",
        "cpu_only": True,
    }


@app.get("/v1/models", dependencies=[Depends(require_api_key)])
def list_models() -> dict[str, object]:
    return {
        "object": "list",
        "data": [
            {
                "id": settings.model_name,
                "object": "model",
                "created": 0,
                "owned_by": "local",
            }
        ],
    }


@app.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    dependencies=[Depends(require_api_key)],
)
def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
    return create_chat_completion(request)
