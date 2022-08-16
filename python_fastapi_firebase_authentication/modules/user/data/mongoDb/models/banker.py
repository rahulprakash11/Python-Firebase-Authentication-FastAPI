from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr


class Address(BaseModel):
    name: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    city: str
    state: str
    pin: str

class Contact(BaseModel):
    phone: Optional[str]
    email: Optional[str]


class Banker(Document):
    
    # ref user table
    userId : PydanticObjectId
    name : str
    address : Optional[Address]
    contact : Contact
    communes : Optional[List[PydanticObjectId]]
    verifiedPhone : Optional[str]
    verifiedEmail : Optional[EmailStr]
    imageUrl : Optional[str]
    status : Optional[int] = None

    class Settings:
        name = "bankers" # mongodb collection name
        

    class Config:
        schema_extra = {
            "example": {
                "userId": "_id",
                "name": "rahul",
                "address": '{"city" : "adj", "state" : "adasd", "pin" : "111111"}',
                "contact": "[phone : 12334454, email : email@email.com]",
                "communes": "[asdfweesd, eawasdffe]",
                "status" : "s"
            }
        }


