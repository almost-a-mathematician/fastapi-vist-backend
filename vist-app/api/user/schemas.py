from datetime import date
from pydantic import BaseModel


class UpdateUser(BaseModel):
    username: str | None
    password: str | None
    # profile_pic в будущем провалидировать вручную (функция в user/endpoints)
    birth_date: date | None
    is_hidden_bd: bool | None
