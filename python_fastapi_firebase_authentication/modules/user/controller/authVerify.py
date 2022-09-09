
from typing import Optional
from fastapi import APIRouter, status, HTTPException
from loguru import logger
from firebase_admin import auth

from ..data.mongoDb.interface.authProvider import MongoDbAuthProvider
from ..data.mongoDb.interface.player import MongoDbPlayer
from ..data.mongoDb.interface.user import MongoDbUser
from ..data.mongoDb.models.authProvider import AuthProvider
from ..data.mongoDb.models.player import Player, Contact
from ..data.mongoDb.models.user import User
from ..constants import UserConstant
from ..data.mongoDb.dbConstants import MongoDbConstant
from ..model.model import AuthorisedUserOut, UserAuthRequest

from ....utils.bitwise import Bitwise


# logger = logging.getLogger(__name__)
 

router = APIRouter()

mongoDbAuthProvider = MongoDbAuthProvider()
mongoDbPlayer = MongoDbPlayer()
mongoDbUser = MongoDbUser()


@router.post("/verify", status_code=status.HTTP_200_OK, response_model=AuthorisedUserOut , response_model_exclude_none=True)
async def verify(pModel : UserAuthRequest):

    try:
        verificationType = pModel.verificationType
        token = pModel.token

        if (
            (verificationType != UserConstant.Auth.VerificationType.player) & 
            (verificationType != UserConstant.Auth.VerificationType.admin)
        ):

            logger.debug(f"--wrong verificationType {verificationType}---")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid verification Type")
        

        deToken : dict = auth.verify_id_token(id_token=token)
        logger.info(deToken)

        pUserId = deToken["user_id"]
        provider :str = deToken["firebase"]["sign_in_provider"] # google.com

        
        if pModel.name:
            name = pModel.name
        else:
            name = deToken.get("name","user")

        # email : str | None
        identifier : Optional[str]
        contact = Contact()

        if provider == MongoDbConstant.AuthProvider.Providers.google: # google.com
            # email = deToken.get("email")
            identifier = deToken.get("email")
            contact.email = identifier
        elif provider == MongoDbConstant.AuthProvider.Providers.phone: # phone
            # phone = deToken.get("phone")
            identifier = deToken.get("phone")
            contact.phone = identifier

        elif provider == MongoDbConstant.AuthProvider.Providers.password: # phone
            # phone = deToken.get("phone")
            identifier = deToken.get("email")
            contact.email = identifier
        else:
            logger.exception(f"---Invalid provider : {provider}---")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid provider")

        dbAuthProvider = await mongoDbAuthProvider.getByIdentifier(identifier=identifier, provider=provider)

        if dbAuthProvider is None:
            
            modelUser = User(
                name=name,
                role=MongoDbConstant.User.Role.player,
                status=MongoDbConstant.User.Status.verified
            )
            dbUser = await mongoDbUser.add(user=modelUser)
            logger.info(f"---user id {dbUser.id}")

            modelAuthProvider = AuthProvider(
                userId=dbUser.id,
                pUid=pUserId,
                credentials=identifier,
                provider=provider,
                authType=MongoDbConstant.AuthProvider.AuthType.firebase
            )
            dbAuthProvider = await mongoDbAuthProvider.add(modelAuth=modelAuthProvider)
            logger.info(f"---created authprovider : {dbAuthProvider}---")

        else:
            logger.debug("---Found dbAuthProvider---")
            userId = dbAuthProvider.userId

            dbUser = await mongoDbUser.getById(id=userId)

            # if status == MongoDbUserConstant.Status.unverified: first get value through masking then check
            if (
                Bitwise().containsValue(
                    originalValue=dbUser.status,
                    maskValue=MongoDbConstant.User.Status.statusMask,
                    checkFor=MongoDbConstant.User.Status.unverified
                )
            ):

                userStatus = Bitwise().attachValue(
                    originalValue=dbUser.status,
                    maskValue=MongoDbConstant.User.Status.unverifiedMask,
                    attachValue=MongoDbConstant.User.Status.verified
                )
                dbUser = await dbUser.set({User.status : userStatus})

            if dbAuthProvider.pUid is None:
                dbAuthProvider = await dbAuthProvider.set({AuthProvider.pUid : pUserId})        

        # get player by uID
        logger.info(f"---user id : {dbAuthProvider.userId}, {dbUser.id}")

        dbPlayer = await mongoDbPlayer.getByUserId(userId=dbUser.id)
        
        if dbPlayer is None:
            if provider == MongoDbConstant.AuthProvider.Providers.google: # google.com
                modelPlayer = Player(userId=dbUser.id, contact=contact, name=name, verifiedEmail=identifier, imageUrl=deToken["picture"])
            elif provider == MongoDbConstant.AuthProvider.Providers.phone: # phone
                modelPlayer = Player(userId=dbUser.id, contact=contact, name=name, verifiedPhone=identifier)
            elif provider == MongoDbConstant.AuthProvider.Providers.password: # phone
                modelPlayer = Player(userId=dbUser.id, contact=contact, name=name, verifiedEmail=identifier)
            else:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED , detail="login method is not set")
            dbPlayer = await mongoDbPlayer.add(player=modelPlayer)
        else:
            if provider == MongoDbConstant.AuthProvider.Providers.google: # google.com
                await dbPlayer.set({Player.verifiedEmail : identifier})
            elif provider == MongoDbConstant.AuthProvider.Providers.phone: # phone
                await dbPlayer.set({Player.verifiedPhone : identifier})
            elif provider == MongoDbConstant.AuthProvider.Providers.password: # phone
                await dbPlayer.set({Player.verifiedEmail : identifier})
            else:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED , detail="login method is not set")

        logger.info(f"---player id : {dbPlayer.id}")

        response = AuthorisedUserOut(user=dbUser, player=dbPlayer)
        return response
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err.args)

