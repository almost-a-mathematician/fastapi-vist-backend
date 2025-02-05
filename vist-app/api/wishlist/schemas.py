from pydantic import BaseModel
from datetime import datetime
from typing import List


class CreateWishlist(BaseModel):
    name: str
    archived_at: datetime | None

class UpdateWishlist(BaseModel):
    name: str | None 
    archived_at: datetime | None

class UpdateWishlistUsers(BaseModel):
    __root__: List[int]




