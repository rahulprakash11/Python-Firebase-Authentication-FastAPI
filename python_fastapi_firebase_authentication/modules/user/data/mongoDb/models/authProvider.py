from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel
import pymongo



class AuthProvider(Document, BaseModel):
    
    userId : PydanticObjectId
    pUid : Optional[str]
    credentials : str
    provider : str
    authType : int
    status : Optional[int]

    class Settings:
        name = "authProviders" # mongodb collection name
        indexes = [
            [
                ("credentials", pymongo.ASCENDING),
                ("authType", pymongo.ASCENDING)
            ]
        ]

    class Config:
        schema_extra = {
            "example": {
                "userId": "_id",
                "pUid": "asdjkjfdsfdjj",
                "credentials": "email@email.com",
                "provider": "firebase",
                "authType": 0x0,
                "status" : None
            }
        }


