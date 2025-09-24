from sqladmin import Admin, ModelView
from main import app
from database import engine
from api.user.models import User
from api.wishlist.models import Wishlist
from api.gift.models import Gift
from api.friend_request.models import FriendRequest
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from api.auth.services.token_manager import access_token
from api.auth.services.password_manager import password_manager
from api.user.services.db import user_service
import os


class AdminAuth(AuthenticationBackend):

	async def login(self, request: Request) -> bool:
		form = await request.form()
		username, password = form['username'], form['password']

		try:
			user = await user_service.get(username=username)
		except:
			return False

		if not user.is_admin:
			return False

		if not password_manager.check(provided_password=password, hashed_password=user.password):
			return False

		access = access_token.create(user.id)

		request.session.update({
			'token': access
		})

		return True

	async def logout(self, request: Request) -> bool:
		request.session.clear()

		return True

	async def authenticate(self, request: Request) -> bool:
		token = request.session.get('token')

		if not token:
			return False

		try:
			payload = access_token.verify(token)
			user = await user_service.get(id=int(payload['sub']))
		except:
			return False

		if not user.is_admin:
			return False

		return True


authentication_backend = AdminAuth(secret_key=os.getenv('ACCESS_TOKEN_SECRET'))
admin = Admin(app, engine, authentication_backend=authentication_backend)


class UserAdmin(ModelView, model=User):
	column_list = [User.id, User.username, User.email, User.friends, User.wishlists]


class WishlistAdmin(ModelView, model=Wishlist):
	column_list = [Wishlist.name, Wishlist.owner, Wishlist.users, Wishlist.gifts, Wishlist.archived_at]


class GiftAdmin(ModelView, model=Gift):
	column_list = [Gift.name, Gift.price, Gift.description, Gift.link_url, Gift.booked_by]


class FriendRequestAdmin(ModelView, model=FriendRequest):
	column_list = [FriendRequest.status, FriendRequest.sender, FriendRequest.receiver, FriendRequest.rejected_by]


admin.add_view(UserAdmin)
admin.add_view(WishlistAdmin)
admin.add_view(GiftAdmin)
admin.add_view(FriendRequestAdmin)
