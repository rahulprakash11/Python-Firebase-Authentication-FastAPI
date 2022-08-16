from fastapi import APIRouter

from ....modules.user.controller import authVerify, banker




userRouter = APIRouter()

userRouter.include_router(authVerify.router, prefix="/auth", tags=["auth"])
userRouter.include_router(banker.router, prefix="/banker", tags=["banker"])

