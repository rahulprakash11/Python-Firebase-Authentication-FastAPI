
from beanie import PydanticObjectId

from ..models.user import User


class MongoDbUser:
    def __init__(self) -> None:        
        self.dbInterface = User

    async def add(self, user : User) -> User:
        dbUser = await user.create()
        return dbUser

    async def getById(self, id : PydanticObjectId) -> User:
        dbUser = await User.get(document_id=id)
        return dbUser

    