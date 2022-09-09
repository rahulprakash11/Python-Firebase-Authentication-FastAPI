
import json
import requests

from fastapi import APIRouter, status, HTTPException
from loguru import logger
from firebase_admin import auth

from ...modules.dummy.model import Login, Register
from ...core.env import WEB_API_KEY
# requests

dummyRouter = APIRouter(prefix="/dummy", tags=["dummy"])


@dummyRouter.post("/register", status_code=status.HTTP_200_OK, response_model_exclude_none=True) # , responses=, response_model=PlayerUpdateOut 
async def create_user(pModel:Register):
    try:
        logger.debug(pModel)
        email = pModel.email
        password = pModel.password

        res = auth.create_user(email=email, email_verified=False, password=password)
        logger.info(res)
        resOut = {"msg" : "Logged in successfully. LOGIN WITH THE REGISTERED CREDETIALS TO GET ACCESS TOKEN TO USE API."}
        return resOut
    except Exception as err:
        logger.info(err.args[0])
        logger.info(type(err.args[0]))
        if "EMAIL_EXISTS" in err.args[0]:
            logger.debug("CAUGHT")
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email already registered!!! Please login.")

        logger.error(err)
        raise err
        
@dummyRouter.post("/login", status_code=status.HTTP_200_OK, response_model_exclude_none=True) # , responses=
async def login_user(pModel:Login):
    try:
        logger.debug(pModel)
        email = pModel.email
        password = pModel.password

        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
        })
        
        r = requests.post(rest_api_url, params={"key": WEB_API_KEY}, data=payload)
        #check for errors in result
        # logger.info(r.json())
        if 'error' in r.json().keys():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'status':'error','message':r.json()['error']['message']})
            # return {'status':'error','message':r.json()['error']['message']}
        #if the registration succeeded
        if 'idToken' in r.json().keys() :
                return {'status':'success','idToken':r.json()['idToken']}

    except Exception as err:
        logger.error(err)
        raise err
