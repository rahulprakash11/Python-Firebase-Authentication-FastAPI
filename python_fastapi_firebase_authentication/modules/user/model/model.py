from typing import Optional
from pydantic import BaseModel
from beanie import PydanticObjectId

from ..data.mongoDb.models.user import User
from ..data.mongoDb.models.player import Player
from ..data.mongoDb.models.player import Address, Player, Contact



class UserAuthRequest(BaseModel):
    token : str
    verificationType : str
    name : Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "token" : "asdfdsiuffdsdfnlasfd6asf5f16dsf4645sdfsdfdsfdsj",
                "verificationType": "player",
                "name" : "rahul"
            }
        }


class AuthorisedUserOut(BaseModel):
    user : User
    player : Player

class UpdateAuthProvider(BaseModel):
    id : PydanticObjectId
    pUid : Optional[str]
    status : Optional[str]




class PlayerUpdate(BaseModel):
    name : Optional[str]
    address : Optional[Address]
    contact : Optional[Contact]
    imageUrl : Optional[str]

class PlayerUpdateOut(BaseModel):
    isUpdated : bool
    item : Player

class UpdateUser(BaseModel):
    id : PydanticObjectId
    name : Optional[str]
    role : Optional[int]
    status : Optional[int]
