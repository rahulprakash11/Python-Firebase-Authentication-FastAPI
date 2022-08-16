# from msilib.schema import Environment
import os
from dotenv import load_dotenv
from loguru import logger

logger.debug(
        f"------Setting up environment!----"
    )

load_dotenv(".env")

TITLE=os.environ.get("TITLE")
ENV = os.environ.get('ENV')
MONGODB_URL=os.environ["MONGODB_URL"]
DB_NAME=os.environ.get("DB_NAME")
DEBUG=os.environ.get("DEBUG", default=True)
GOOGLE_APPLICATION_CREDENTIALS=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
ALLOWED_ORIGINS=os.environ.get("CORS_ALLOWED_ORIGINS").split(",")

UVI_PORT=int(os.environ.get("UVI_PORT", default=8000))
UVI_SERVER_HOST=os.environ.get("UVI_SERVER_HOST", default="0.0.0.0")
UVI_LOG_LEVEL=os.environ.get("UVI_LOG_LEVEL", default="info")
UVI_ACCESS_LOG=os.environ.get("UVI_ACCESS_LOG", default=False)

logger.info(
        f"------Working inside {ENV} environment!----"
    )

logger.info(
        f"------ALLOWED_ORIGINS : {ALLOWED_ORIGINS}, {type(ALLOWED_ORIGINS)}----"
    )
