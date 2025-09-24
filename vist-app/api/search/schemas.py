from pydantic import BaseModel
from typing import List
from api.user.schemas import UserSerializer
from api.wishlist.schemas import WishlistSerializer


class SearchSerializer(BaseModel):
    users: List[UserSerializer]
    wishlists: List[WishlistSerializer]