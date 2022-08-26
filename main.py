
from firebase_admin import initialize_app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from python_fastapi_firebase_authentication.core.env import TITLE, DEBUG, ALLOWED_ORIGINS, BASE_DIR
from python_fastapi_firebase_authentication.core.custom_logging import CustomizeLogger
from python_fastapi_firebase_authentication.core.data.mongodb.db import init_db, mongodb_client
from python_fastapi_firebase_authentication.modules.user.route.endpoints import userRouter
from python_fastapi_firebase_authentication.modules.dummy.endpoints import dummyRouter


# logger = logging.getLogger(__name__)

config_path=BASE_DIR.with_name("logging_config.json")


app = FastAPI(title=TITLE, debug=DEBUG)
logger = CustomizeLogger.make_logger(config_path)
app.logger = logger

@app.get("/")
def read_root():
    return {"Hello App Users": "Welcome to the app!"}


app.include_router(router=userRouter)
app.include_router(router=dummyRouter)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... some code skipped

@app.on_event("startup")
async def app_init():
    logger.debug("---Initializing the database---")
    await init_db(mongodb_client)
    initialize_app()
    logger.debug("---The Database setup is complete!---")
