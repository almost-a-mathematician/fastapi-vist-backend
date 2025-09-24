from sqlalchemy import or_, select
from api.friend_request.models import FriendRequest
from api.user.models import user_friend_association
from database import AsyncSessionMaker, Session
from api.user.models import User
from api.user.services.db import UserDoesNotExistException
from sqlalchemy.orm import selectinload


class FriendRequestPermissionException(BaseException):
	...


class FriendRequestDoesNotExistException(BaseException):
	...


class FriendRequestService:

	def __init__(self, Session: AsyncSessionMaker):
		self.Session = Session

	async def get(self, user: User):
		async with self.Session() as session:

			query = select(FriendRequest).where(
				or_((FriendRequest.sender_id == user.id),
				(FriendRequest.receiver_id == user.id))
			).options(
				selectinload(FriendRequest.sender),
				selectinload(FriendRequest.receiver),
				selectinload(FriendRequest.rejected_by)
			)

			friend_request = (await session.scalars(query)).all()

			return friend_request

	async def create(self, id: int, user: User, status: str):
		async with self.Session() as session:

			if user.id == id:
				raise FriendRequestPermissionException

			receiver = await session.get(User, id)

			if receiver is None:
				raise UserDoesNotExistException

			does_request_exist = select(FriendRequest).where(
				or_((FriendRequest.receiver_id == id) & (FriendRequest.sender_id == user.id),
				(FriendRequest.sender_id == id) & (FriendRequest.receiver_id == user.id))
			)

			existing_request = await session.scalars(does_request_exist)
			if existing_request.first() is not None:
				raise FriendRequestPermissionException

			friend_request = FriendRequest(sender_id=user.id, receiver_id=id, status=status)

			session.add(friend_request)
			await session.commit()
			await session.refresh(friend_request, attribute_names=FriendRequest.get_all_columns())

			return friend_request

	async def update(self, id: int, user: User, status: str):
		async with self.Session() as session:

			friend_request = await session.get(
				FriendRequest,
				id,
				options=[
				selectinload(FriendRequest.sender),
				selectinload(FriendRequest.receiver),
				selectinload(FriendRequest.rejected_by)
				]
			)

			if status == 'accepted':
				if (friend_request.status == 'sent'
					and friend_request.receiver_id == user.id) or (friend_request.status == 'rejected'
					and friend_request.rejected_by_id == user.id):
					friend_request.status = status
				else:
					raise FriendRequestPermissionException

			elif status == 'rejected':
				if friend_request.status == 'accepted' or (friend_request.status == 'sent'
					and friend_request.receiver_id == user.id):
					friend_request.status = status
					friend_request.rejected_by_id = user.id
				else:
					raise FriendRequestPermissionException

			await session.commit()
			await session.refresh(friend_request, attribute_names=FriendRequest.get_all_columns())

			return friend_request

	async def delete(self, id: int, user: User):
		async with self.Session() as session:

			friend_request = await session.get(FriendRequest, id)

			if friend_request is None:
				raise FriendRequestDoesNotExistException

			if friend_request.status == 'sent' and friend_request.sender_id == user.id:
				await session.delete(friend_request)
				await session.commit()
			else:
				raise FriendRequestPermissionException

			return True


friend_request_service = FriendRequestService(Session)
