from database import Session
from sqlalchemy import select
from api.friend_request.models import FriendRequest
from api.user.models import user_friend_association

class FriendRequestService:
    ...