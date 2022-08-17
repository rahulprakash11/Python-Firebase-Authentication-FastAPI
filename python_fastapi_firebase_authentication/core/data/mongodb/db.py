from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from ...env import DB_NAME, MONGODB_URL

from ....modules.user.data.mongoDb.models.authProvider import AuthProvider
from ....modules.user.data.mongoDb.models.player import Player
from ....modules.user.data.mongoDb.models.user import User


__models = [
    AuthProvider,
    User,
    Player
]

mongodb_client:AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URL)

# logger.info(client.db) 


async def init_db(client:AsyncIOMotorClient):
    # client = AsyncIOMotorClient(MONGODB_URL)
    await init_beanie(client[DB_NAME], document_models=__models)

async def close_db(client:AsyncIOMotorClient):
    # client = AsyncIOMotorClient(MONGODB_URL)
    logger.info("Closing connection to MongoDB")
    await client.close()
    logger.info("MongoDB connection closed")