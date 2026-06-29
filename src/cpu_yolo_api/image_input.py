import base64
import binascii
from dataclasses import dataclass
from io import BytesIO

from fastapi import HTTPException, status
from PIL import Image, UnidentifiedImageError

from cpu_yolo_api.config import settings
from cpu_yolo_api.schemas import ChatCompletionRequest

ALLOWED_PREFIXES = {
    "data:image/jpeg;base64,": "image/jpeg",
    "data:image/jpg;base64,": "image/jpeg",
    "data:image/png;base64,": "image/png",
}


@dataclass(frozen=True)
class DecodedImage:
    media_type: str
    data: bytes
    width: int
    height: int


def extract_single_base64_image(request: ChatCompletionRequest) -> DecodedImage:
    """Extract exactly one base64 data URL image from an OpenAI-style chat request."""

    image_urls: list[str] = []

    for message in request.messages:
        if isinstance(message.content, str):
            continue

        for part in message.content:
            if part.type == "image_url" and part.image_url is not None:
                image_urls.append(part.image_url.url)

    if not image_urls:
        _bad_request("Exactly one base64 image data URL is required.", "missing_image")

    if len(image_urls) > 1:
        _bad_request("Exactly one image is allowed per request.", "multiple_images")

    return decode_base64_image_data_url(image_urls[0])


def decode_base64_image_data_url(data_url: str) -> DecodedImage:
    """Decode and validate a supported base64 image data URL."""

    if data_url.startswith(("http://", "https://")):
        _bad_request("Remote image URLs are not supported in the MVP.", "remote_url_not_supported")

    matched_prefix = None
    media_type = None

    for prefix, candidate_media_type in ALLOWED_PREFIXES.items():
        if data_url.startswith(prefix):
            matched_prefix = prefix
            media_type = candidate_media_type
            break

    if matched_prefix is None or media_type is None:
        _bad_request(
            "Unsupported image input. Use a jpeg or png base64 data URL.",
            "unsupported_image_input",
        )

    encoded = data_url[len(matched_prefix):]

    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        _bad_request("Invalid base64 image data.", "invalid_base64")

    if len(raw) > settings.max_image_bytes:
        _bad_request("Image is larger than the configured size limit.", "image_too_large")

    try:
        with Image.open(BytesIO(raw)) as image:
            image.verify()

        with Image.open(BytesIO(raw)) as image:
            width, height = image.size
    except (UnidentifiedImageError, OSError, ValueError):
        _bad_request("Image data could not be decoded.", "invalid_image")

    return DecodedImage(
        media_type=media_type,
        data=raw,
        width=width,
        height=height,
    )


def _bad_request(message: str, code: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "error": {
                "message": message,
                "type": "invalid_request_error",
                "code": code,
            }
        },
    )
