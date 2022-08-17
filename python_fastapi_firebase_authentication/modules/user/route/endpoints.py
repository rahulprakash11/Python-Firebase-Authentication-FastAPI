from fastapi import APIRouter

from ....modules.user.controller import authVerify, player




userRouter = APIRouter()

userRouter.include_router(authVerify.router, prefix="/auth", tags=["auth"])
userRouter.include_router(player.router, prefix="/player", tags=["player"])

