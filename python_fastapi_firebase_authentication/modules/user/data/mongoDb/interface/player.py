
from beanie import PydanticObjectId
from loguru import logger

from ..models.player import Player
from ....model.model import PlayerUpdate


class MongoDbPlayer:

    async def add(self, player : Player) -> Player:
        player = await player.create()
        return player

    async def update(self, dbPlayer:Player, pModel:PlayerUpdate) -> Player:
        try:
            logger.debug(dbPlayer)
            await dbPlayer.set(expression=pModel.dict(exclude_unset=True))
            logger.debug(dbPlayer)
            return dbPlayer
        except Exception as err:
            logger.error('error in', err)
            raise err


    async def getById(self, id : PydanticObjectId) -> Player:
        try:
            player = await Player.get(document_id=id)
            return player
        except Exception as err:
            raise err
        
    async def getByUserId(self, userId : PydanticObjectId) -> Player:
        logger.info(userId)
        player = await Player.find(Player.userId == userId).first_or_none()
        # logger.info(player.id)
        return player

