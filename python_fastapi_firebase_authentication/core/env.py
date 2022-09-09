
from loguru import logger

from .settings import settings, BASE_DIR


TITLE = settings.TITLE
SECRET_KEY = settings.SECRET_KEY
WEB_API_KEY = settings.WEB_API_KEY
ENV = settings.ENV
MONGODB_URL = settings.MONGODB_URL
DB_NAME = settings.DB_NAME
DEBUG = settings.FASTAPI_DEBUG
ALLOWED_ORIGINS = settings.CORS_ALLOWED_ORIGINS.split(",")
LOGGING_CONFIG_PATH = BASE_DIR.with_name("logging_config.json")

UVI_PORT = settings.UVI_PORT
UVI_SERVER_HOST = settings.UVI_SERVER_HOST
UVI_RELOAD = settings.UVI_RELOAD
UVI_LOG_LEVEL = settings.UVI_LOG_LEVEL
UVI_ACCESS_LOG = settings.UVI_ACCESS_LOG


logger.info(f"------Working inside {settings.ENV} environment!----")
