from beanie import PydanticObjectId
from fastapi import Depends, APIRouter, status, HTTPException
from loguru import logger

from ...user.data.mongoDb.interface.player import MongoDbPlayer
from ...user.data.mongoDb.models.player import Player
from ...user.model.model import PlayerUpdate, PlayerUpdateOut
from ....utils.dependencies import currentPlayer



router = APIRouter()

mongoDbPlayer = MongoDbPlayer()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Player , response_model_exclude_none=True) # , responses=
async def getPlayer(id :PydanticObjectId, currentPlayer : Player = Depends(currentPlayer)):
    try:
        objectId = id
        if objectId == currentPlayer.id:
            response = currentPlayer
            return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg":"Referenced Player not found", "id":objectId})
    except Exception as err:
        logger.error(err)
        raise err



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PlayerUpdateOut , response_model_exclude_none=True) # , responses=
async def updatePlayer(id :PydanticObjectId, pModel:PlayerUpdate, currentPlayer : Player = Depends(currentPlayer)):
    try:
        logger.debug(id)
        logger.debug(currentPlayer.id)
        objectId = id
        if objectId != currentPlayer.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg" : "Not Authorised. Can update only self player info."})

        dbPlayer = await mongoDbPlayer.update(dbPlayer=currentPlayer, pModel=pModel)
        response = PlayerUpdateOut(isUpdated=True, item=dbPlayer)

        logger.debug(response)
        return response
    except HTTPException as err:
        logger.error(err.detail)
        raise err
    except Exception as err:
        logger.error(err)
        raise err
    