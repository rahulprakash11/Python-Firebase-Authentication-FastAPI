from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from typing import Optional
from pydantic import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.with_name(".env"))


class GlobalConfig(BaseSettings):
    """Global configurations."""
    TITLE : str
    SECRET_KEY : Optional[str]
    WEB_API_KEY : Optional[str]
    MONGODB_URL : Optional[str]
    DB_NAME : Optional[str]
    FASTAPI_DEBUG : bool = False
    CORS_ALLOWED_ORIGINS : str

    UVI_PORT : Optional[int] = None
    UVI_SERVER_HOST : Optional[str] = None
    UVI_RELOAD : Optional[bool] = False
    UVI_LOG_LEVEL : Optional[str] = "info"
    UVI_ACCESS_LOG : Optional[bool] = False
    ENV : str


@lru_cache()
def get_settings():
    return GlobalConfig()


settings = get_settings()