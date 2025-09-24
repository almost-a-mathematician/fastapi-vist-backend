from typing import Literal
from pydantic import BaseModel
from typing import List
from api.user.schemas import UserSerializer


class CreateUserFriend(BaseModel):
    receiver_id: int
    status: Literal['sent']
    
class UpdateRequestStatus(BaseModel):
    status: Literal['accepted', 'rejected']

class FriendRequestSerializer(BaseModel):
    id: int
    status: Literal['sent', 'accepted', 'rejected']
    sender: UserSerializer
    receiver: UserSerializer
    rejected_by: UserSerializer | None = None

class FriendRequestsListSerializer(BaseModel):
    items: List[FriendRequestSerializer]

