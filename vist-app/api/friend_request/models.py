from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from enum import Enum
from api.user.models import User
from sqlalchemy import ForeignKey


class Status(str, Enum):
	sent = 'sent'
	accepted = 'accepted'
	rejected = 'rejected'


class FriendRequest(Model):
	__tablename__ = 'friend_requests'

	status: Mapped[Status] = mapped_column(nullable=False)
	sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
	sender: Mapped[User] = relationship(
		foreign_keys=sender_id,
		backref=backref("friend_requests_sent",
		cascade='all, delete')
	)
	receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
	receiver: Mapped[User] = relationship(
		foreign_keys=receiver_id,
		backref=backref("friend_request_received",
		cascade='all, delete')
	)
	rejected_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
	rejected_by: Mapped[User | None] = relationship(
		foreign_keys=rejected_by_id,
		backref=backref("friend_requests_rejected",
		cascade='all, delete')
	)

	@classmethod
	def get_all_columns(cls):
		return cls.__table__.columns.keys() + ['sender', 'receiver', 'rejected_by']
