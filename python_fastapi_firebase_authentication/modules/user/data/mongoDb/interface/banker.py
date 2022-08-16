
from beanie import PydanticObjectId
from loguru import logger

from ..models.banker import Banker
from ....model.banker import BankerUpdate


class MongoDbBanker:

    async def add(self, banker : Banker) -> Banker:
        banker = await banker.create()
        return banker

    async def update(self, dbBanker:Banker, pModel:BankerUpdate) -> Banker:
        try:
            logger.debug(dbBanker)
            await dbBanker.set(expression=pModel.dict(exclude_unset=True))
            logger.debug(dbBanker)
            return dbBanker
        except Exception as err:
            logger.error('error in', err)
            raise err


    async def getById(self, id : PydanticObjectId) -> Banker:
        try:
            banker = await Banker.get(document_id=id)
            return banker
        except Exception as err:
            raise err
        
    async def getByUserId(self, userId : PydanticObjectId) -> Banker:
        logger.info(userId)
        banker = await Banker.find(Banker.userId == userId).first_or_none()
        # logger.info(banker.id)
        return banker

