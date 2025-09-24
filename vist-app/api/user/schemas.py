from datetime import date
from pydantic import BaseModel, EmailStr, field_serializer
from typing import List


class UpdateUser(BaseModel):
	username: str | None = None
	password: str | None = None
	birth_date: date | None = None
	is_hidden_bd: bool | None = None


class UserSerializer(BaseModel):
	id: int
	username: str
	profile_pic: str | None
	birth_date: date | None
	is_hidden_bd: bool
	email: EmailStr | None

	@field_serializer('email')
	def serialize_email(self, email, info):
		try:
			auth_user_id = info.context.get('auth_user_id')
			if auth_user_id is None:
				raise Exception

			return email if auth_user_id == self.id else None

		except:
			raise Exception('Context is not defined')

	@field_serializer('birth_date')
	def serialize_birth_date(self, birth_date, info):
		try:
			auth_user_id = info.context.get('auth_user_id')
			if auth_user_id is None:
				raise Exception

			return str(birth_date) if self.is_hidden_bd == False or auth_user_id == self.id else None

		except:
			raise Exception('Context is not defined')


class FullUserSerializer(UserSerializer):
	friends: List[UserSerializer]
