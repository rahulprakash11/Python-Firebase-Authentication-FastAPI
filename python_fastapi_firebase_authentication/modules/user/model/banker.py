
from typing import Optional
from pydantic import BaseModel

from ..data.mongoDb.models.banker import Address, Banker, Contact


class BankerUpdate(BaseModel):
    name : Optional[str]
    address : Optional[Address]
    contact : Optional[Contact]
    imageUrl : Optional[str]

class BankerUpdateOut(BaseModel):
    isUpdated : bool
    item : Banker

