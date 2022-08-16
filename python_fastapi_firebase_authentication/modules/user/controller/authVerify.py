
from typing import Optional
from fastapi import APIRouter, status, HTTPException
from loguru import logger
from firebase_admin import auth

from ..data.mongoDb.interface.authProvider import MongoDbAuthProvider
from ..data.mongoDb.interface.banker import MongoDbBanker
from ..data.mongoDb.interface.user import MongoDbUser
from ..data.mongoDb.models.authProvider import AuthProvider
from ..data.mongoDb.models.banker import Banker, Contact
from ..data.mongoDb.models.user import User
from ..constants import UserConstant
from ..data.mongoDb.dbConstants import MongoDbConstant
from ..model.authorisedUser import AuthorisedUserOut, UserAuthRequest

from ....utils.bitwise import Bitwise


# logger = logging.getLogger(__name__)
 

router = APIRouter()

mongoDbAuthProvider = MongoDbAuthProvider()
mongoDbBanker = MongoDbBanker()
mongoDbUser = MongoDbUser()


@router.post("/verify",tags=["verify"] , status_code=status.HTTP_200_OK, response_model=AuthorisedUserOut , response_model_exclude_none=True)
async def verify(pModel : UserAuthRequest):

    try:
        verificationType = pModel.verificationType
        token = pModel.token

        if (
            (verificationType != UserConstant.Auth.VerificationType.banker) & 
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
        else:
            logger.exception(f"---Invalid provider : {provider}---")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid provider")

        dbAuthProvider = await mongoDbAuthProvider.getByIdentifier(identifier=identifier, provider=provider)

        if dbAuthProvider is None:
            
            modelUser = User(
                name=name,
                role=MongoDbConstant.User.Role.banker,
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

        # get banker by uID
        logger.info(f"---user id : {dbAuthProvider.userId}, {dbUser.id}")

        dbBanker = await mongoDbBanker.getByUserId(userId=dbUser.id)
        
        if dbBanker is None:
            if provider == MongoDbConstant.AuthProvider.Providers.google: # google.com
                modelBanker = Banker(userId=dbUser.id, contact=contact, name=name, verifiedEmail=identifier, imageUrl=deToken["picture"])
            elif provider == MongoDbConstant.AuthProvider.Providers.phone: # phone
                modelBanker = Banker(userId=dbUser.id, contact=contact, name=name, verifiedPhone=identifier) 
            dbBanker = await mongoDbBanker.add(banker=modelBanker)
        else:
            if provider == MongoDbConstant.AuthProvider.Providers.google: # google.com
                await dbBanker.set({Banker.verifiedEmail : identifier})
            elif provider == MongoDbConstant.AuthProvider.Providers.phone: # phone
                await dbBanker.set({Banker.verifiedPhone : identifier})  
        
        
        logger.info(f"---banker id : {dbBanker.id}")

        response = AuthorisedUserOut(user=dbUser, banker=dbBanker)
        return response

    except Exception as err:
        logger.error(err)
        raise err

