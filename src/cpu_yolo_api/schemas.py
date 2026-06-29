from typing import Any, Literal

from pydantic import BaseModel, Field


class ImageURL(BaseModel):
    url: str


class ContentPart(BaseModel):
    type: str
    text: str | None = None
    image_url: ImageURL | None = None


class ChatMessage(BaseModel):
    role: str
    content: str | list[ContentPart]


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool | None = None


class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class Detection(BaseModel):
    class_name: str = Field(serialization_alias="class")
    confidence: float
    box: Box


class DetectionPayload(BaseModel):
    detections: list[Detection]
    image: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatCompletionChoice(BaseModel):
    index: int
    message: dict[str, str]
    finish_reason: Literal["stop"] = "stop"


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"] = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: dict[str, int] = Field(default_factory=lambda: {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    })
