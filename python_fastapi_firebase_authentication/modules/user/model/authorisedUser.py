from typing import Optional
from pydantic import BaseModel
from beanie import PydanticObjectId

from ..data.mongoDb.models.user import User
from ..data.mongoDb.models.banker import Banker



class UserAuthRequest(BaseModel):
    token : str
    verificationType : str
    name : Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "token" : "asdfdsiuffdsdfnlasfd6asf5f16dsf4645sdfsdfdsfdsj",
                "verificationType": "banker",
                "name" : "rahul"
            }
        }


class AuthorisedUserOut(BaseModel):
    user : User
    banker : Banker

class UpdateAuthProvider(BaseModel):
    id : PydanticObjectId
    pUid : Optional[str]
    status : Optional[str]