from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, Header, status
from firebase_admin import auth
from loguru import logger

from ..modules.user.data.mongoDb.interface.authProvider import MongoDbAuthProvider
from ..modules.user.data.mongoDb.interface.player import MongoDbPlayer

mongoDbAuthProvider = MongoDbAuthProvider()
mongoDbPlayer = MongoDbPlayer()

async def decodeToken(token : str = Header()):
    try:
        deToken : dict = auth.verify_id_token(id_token=token)
        pUserId:str = deToken.get("user_id")
        dbAuthProvider = await mongoDbAuthProvider.getByProviderUserId(pUserId=pUserId)
        userId = dbAuthProvider.userId
        return userId
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")


async def currentPlayer(userId : PydanticObjectId = Depends(decodeToken)):
    player = await mongoDbPlayer.getByUserId(userId=userId)
    return player
