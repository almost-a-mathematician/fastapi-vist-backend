from pydantic import BaseModel
from typing import List
from api.user.schemas import UserResponse
from api.wishlist.schemas import WishlistSerializer


class SearchResponse(BaseModel):
    users: List[UserResponse]
    wishlists: List[WishlistSerializer]