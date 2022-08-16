from beanie import PydanticObjectId
from fastapi import Depends, APIRouter, status, HTTPException
from loguru import logger

from ...user.data.mongoDb.interface.banker import MongoDbBanker
from ...user.data.mongoDb.models.banker import Banker
from ...user.model.banker import BankerUpdate, BankerUpdateOut
from ....utils.dependencies import currentBanker



router = APIRouter()

mongoDbBanker = MongoDbBanker()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Banker , response_model_exclude_none=True) # , responses=
async def getBanker(id :PydanticObjectId, currentBanker : Banker = Depends(currentBanker)):
    try:
        objectId = id
        if objectId == currentBanker.id:
            response = currentBanker
            return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"Referenced Banker not found", "id":objectId})
    except Exception as err:
        logger.error(err)
        raise err



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=BankerUpdateOut , response_model_exclude_none=True) # , responses=
async def updateBanker(id :PydanticObjectId, pModel:BankerUpdate, currentBanker : Banker = Depends(currentBanker)):
    try:
        logger.debug(id)
        logger.debug(currentBanker.id)
        objectId = id
        if objectId != currentBanker.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg" : "Not Authorised. Can update only self banker info."})

        dbBanker = await mongoDbBanker.update(dbBanker=currentBanker, pModel=pModel)
        response = BankerUpdateOut(isUpdated=True, item=dbBanker)

        logger.debug(response)
        return response
    except HTTPException as err:
        logger.error(err.detail)
        raise err
    except Exception as err:
        logger.error(err)
        raise err
    