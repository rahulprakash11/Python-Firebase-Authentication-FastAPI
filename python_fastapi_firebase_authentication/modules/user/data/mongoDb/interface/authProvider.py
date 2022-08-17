
from typing import Optional
from beanie import PydanticObjectId
# from loguru import logger

from ..models.authProvider import AuthProvider
from ....model.model import UpdateAuthProvider


class MongoDbAuthProvider:

    async def add(self, modelAuth : AuthProvider) -> AuthProvider:
        authUser = await modelAuth.create()
        return authUser

    async def getByProviderUserId(self, pUserId : PydanticObjectId) -> AuthProvider:
        authUser = await AuthProvider.find(AuthProvider.pUid == pUserId).first_or_none()
        return authUser
        
    async def getByIdentifier(self, identifier : str, provider : Optional[str]) -> AuthProvider:
        authUser = await AuthProvider.find(AuthProvider.credentials == identifier).find(AuthProvider.provider == provider).first_or_none()
        return authUser

    async def updateSelf(self, updateModel:UpdateAuthProvider) -> AuthProvider:
        authUser = await AuthProvider.get(document_id=updateModel.id)
        authUser = authUser.copy(update=updateModel.dict(exclude_unset=True))
        await authUser.save()
        return authUser


