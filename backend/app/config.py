from typing import List, Optional, Union
import json
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database SQLite Async (lưu tại thư mục backend/)
    DATABASE_URL: str = "sqlite+aiosqlite:///./forfriend.db"

    # JWT
    JWT_SECRET_KEY: str = "super-secret-key-forfriend-dev-only-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # LiveKit (Cloud Free Tier)
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    LIVEKIT_URL: str = "wss://your-app.livekit.cloud"

    # Gemini AI OCR for Student ID Verification
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024     # 5MB
    MAX_CV_SIZE: int = 10 * 1024 * 1024        # 10MB

    # CORS — Cho phép cả Localhost lẫn IP mạng LAN
    CORS_ORIGINS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
