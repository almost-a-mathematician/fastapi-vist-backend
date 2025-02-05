from pydantic import BaseModel
from api.friend_request.models import Status


class CreateUserFriend(BaseModel):
    receiver_id: int

class ChangeRequestStatus(BaseModel):
    status: Status
    