
from pathlib import Path
from firebase_admin import initialize_app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.env import TITLE, DEBUG, ALLOWED_ORIGINS
from .core.custom_logging import CustomizeLogger
from .core.data.mongodb.db import close_db, init_db, mongodb_client
from .modules.user.route.endpoints import userRouter


# logger = logging.getLogger(__name__)

config_path=Path(__file__).parent.with_name("logging_config.json")


app = FastAPI(title=TITLE, debug=DEBUG)
logger = CustomizeLogger.make_logger(config_path)
app.logger = logger

@app.get("/")
def read_root():
    return {"Hello App Users": "Welcome to the app!"}


app.include_router(router=userRouter)


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

 
@app.on_event("shutdown")
async def shutdown():
    logger.info("db connection shutdown")
    await close_db(mongodb_client)
    logger.info("MongoDB connection closed")
