from typing import List
from pydantic import BaseModel, HttpUrl
from api.user.schemas import UserSerializer


class СreateGift(BaseModel):
    name: str
    price: float
    description: str | None = None
    link_url: HttpUrl
    is_priority: bool = None
    
class UpdateGift(BaseModel):
    name: str = None
    price: float = None
    description: str | None = None
    link_url: HttpUrl = None
    is_priority: bool = None

class BookGift(BaseModel):
    booked_by: int | None 
    
class GiftIconSerializer(BaseModel):
    id: int
    img: str | None

class GiftSerializer(GiftIconSerializer):
    link_url: str
    is_priority: bool
    booked_by: UserSerializer | None 

class FullGiftSerializer(GiftSerializer): 
    name: str
    price: float
    description: str | None
    wishlist_id: int

class FullGiftsListSerializer(BaseModel):
    items: List[FullGiftSerializer]


