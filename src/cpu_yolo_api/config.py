from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_key: str = Field(default="dev-secret-change-me", alias="YOLO_API_KEY")
    model_name: str = Field(default="cpu-yolo-detector", alias="YOLO_MODEL_NAME")
    max_image_bytes: int = Field(default=10 * 1024 * 1024, alias="YOLO_MAX_IMAGE_BYTES")
    mock_detector: bool = Field(default=True, alias="YOLO_MOCK_DETECTOR")


settings = Settings()
