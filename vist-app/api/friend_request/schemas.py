from typing import Literal
from pydantic import BaseModel
from typing import List
from api.user.schemas import UserResponse

class FriendRequestResponse(BaseModel):
    id: int
    status: Literal['sent', 'accepted', 'rejected']
    sender: UserResponse
    receiver: UserResponse
    rejected_by: UserResponse | None = None

class FriendRequestsResponse(BaseModel):
    items: List[FriendRequestResponse]

class CreateUserFriend(BaseModel):
    receiver_id: int
    status: Literal['sent']

class UpdateRequestStatus(BaseModel):
    status: Literal['accepted', 'rejected']
    
