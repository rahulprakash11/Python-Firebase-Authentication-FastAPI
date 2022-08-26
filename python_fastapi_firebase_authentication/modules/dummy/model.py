
from typing import Optional
from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email : Optional[EmailStr] = "dummy@email.com"
    password : Optional[str] = "password"

class Register(BaseModel):
    email : Optional[EmailStr] = "dummy@email.com"
    password : Optional[str] = "password"