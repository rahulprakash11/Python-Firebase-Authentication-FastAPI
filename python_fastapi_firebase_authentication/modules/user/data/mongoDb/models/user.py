
from beanie import Document


# role -> 0 : admin, 1 : player
# status -> 0 : inactive, 1 : active


class User(Document):
    
    name : str
    role : int
    status : int

    class Settings:
        name = "users" # mongodb collection name

    class Config:
        schema_extra = {
            "example": {
                "Id": "_id",
                "name":"rahul",
                "role": 1,
                "status" : 1
            }
        }
