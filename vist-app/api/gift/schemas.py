from typing import List
from pydantic import BaseModel, HttpUrl
from api.user.schemas import UserResponse


class СreateGift(BaseModel):
    name: str
    # img??? в будущем провалидировать вручную (функция в gift/endpoints)
    price: float
    description: str | None = None
    link_url: HttpUrl
    is_priority: bool = None
    
class UpdateGift(BaseModel):
    name: str = None
    # img: bytes = None
    price: float = None
    description: str | None = None
    link_url: HttpUrl = None
    is_priority: bool = None
    
class GiftIcon(BaseModel):
    id: int
    img: str | None

class GiftResponse(GiftIcon):
    link_url: str
    is_priority: bool
    booked_by: UserResponse | None 

class GiftFullResponse(GiftResponse): 
    name: str
    price: float
    description: str | None
    wishlist_id: int

class GiftsFullResponse(BaseModel):
    items: List[GiftFullResponse]

class BookGift(BaseModel):
    booked_by: int | None 

