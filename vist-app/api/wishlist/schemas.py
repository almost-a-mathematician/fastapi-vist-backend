from pydantic import BaseModel, field_serializer, RootModel, field_validator
from datetime import datetime
from typing import List
from api.user.schemas import UserSerializer
from api.gift.schemas import GiftIconSerializer


class ArchivedAtField():
    archived_at: datetime | None = None

    @field_validator('archived_at', mode='before')
    def archived_at_time(cls, value) -> datetime:
        return None if value is None else datetime.now()
              
class CreateWishlist(BaseModel, ArchivedAtField):
    name: str

class UpdateWishlist(BaseModel, ArchivedAtField):
    name: str = None

class UpdateWishlistUsers(RootModel):
    root: List[int]

class WishlistSerializer(BaseModel):
    id: int
    name: str
    users: List[UserSerializer]
    gifts: List[GiftIconSerializer]
    owner_id: int
    archived_at: datetime | None

    @field_serializer('gifts')
    def serialize_gifts(self, gifts: List['GiftIconSerializer']):
        return gifts[:4]
    
    @field_serializer('archived_at')
    def serialize_archived_at(self, archived_at: datetime | None):
        return None if archived_at is None else str(archived_at)

    @field_serializer('users')
    def serialize_users(self, users, info):
        try:
            auth_user_id = info.context.get('auth_user_id')
            if auth_user_id is None:
                raise Exception
            
            return users if auth_user_id == self.owner_id else []
        except:
            raise Exception('Context is not defined')
        
class WishlistsListSerializer(BaseModel):
    items: List[WishlistSerializer]
