from datetime import date
from pydantic import BaseModel, EmailStr


class UpdateUser(BaseModel):
    username: str | None
    password: str | None
    # profile_pic в будущем провалидировать вручную (функция в user/endpoints)
    birth_date: date | None
    is_hidden_bd: bool | None

class UserResponse(BaseModel):
    id: int
    username: str
    profile_pic: str | None
    birth_date: date | None
    # friends

class UserFullResponse(UserResponse):
    email: EmailStr
    is_hidden_bd: bool