from pydantic import BaseModel, field_serializer, RootModel
from datetime import datetime
from typing import List
from api.user.schemas import UserResponse


class CreateWishlist(BaseModel):
    name: str
    archived_at: datetime | None

class UpdateWishlist(BaseModel):
    name: str | None 
    archived_at: datetime | None

class UpdateWishlistUsers(RootModel):
    root: List[int]

class WishlistSerializer(BaseModel):
    name: str
    users: List[UserResponse]
    owner_id: int
    archived_at: datetime

    @field_serializer('users')
    def serialize_users(self, users, info):
        try:
            auth_user_id = info.context.get('auth_user_id')
            if auth_user_id == None:
                raise Exception
            
            return users if auth_user_id == self.owner_id else []
        except:
            raise Exception('Context is not defined')
        
class WishlistsSerializer(BaseModel):
    items: List[WishlistSerializer]
