
from loguru import logger
from firebase_admin import initialize_app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from python_fastapi_firebase_authentication.core.env import TITLE, DEBUG, ALLOWED_ORIGINS, LOGGING_CONFIG_PATH
from python_fastapi_firebase_authentication.core.custom_logging import CustomizeLogger
from python_fastapi_firebase_authentication.core.data.mongodb.db import init_db, mongodb_client
from python_fastapi_firebase_authentication.modules.user.route.endpoints import userRouter
from python_fastapi_firebase_authentication.modules.dummy.endpoints import dummyRouter


def get_application():
    _app = FastAPI(title=TITLE, debug=DEBUG)

    logger = CustomizeLogger.make_logger(LOGGING_CONFIG_PATH)
    _app.logger = logger
    _app.include_router(router=userRouter)
    _app.include_router(router=dummyRouter)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],#ALLOWED_ORIGINS
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app

app = get_application()
# ... some code skipped

@app.get("/")
def read_root():
    return {"Hello App Users": "Welcome to the app!"}


@app.on_event("startup")
async def app_init():
    logger.debug("---Initializing---")
    await init_db(mongodb_client)
    logger.debug("---Initialized the database---")
    initialize_app()
    logger.debug("---Initialized the firebase admin---")
