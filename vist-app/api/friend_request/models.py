from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from api.user.models import User
from sqlalchemy import ForeignKey


class Status(str, Enum):
    sent = 'Sent'
    accepted = 'Accepted'
    rejected = 'Rejected'

class FriendRequest(Model):
    __tablename__ = 'friend_requests'

    status: Mapped[Status] = mapped_column(nullable=False)
    sender: Mapped[User] = relationship( cascade='all, delete')
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    receiver: Mapped[User] = relationship(cascade='all, delete')
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rejected_by: Mapped[User | None] = relationship(cascade='all, delete')
    rejected_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    