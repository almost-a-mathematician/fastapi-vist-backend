from pydantic import BaseModel, HttpUrl


class СreateGift(BaseModel):
    name: str
    # img??? в будущем провалидировать вручную (функция в gift/endpoints)
    price: float
    description: str | None
    link_url: HttpUrl
    is_priority: bool | None
    
class UpdateGift(BaseModel):
    name: str | None
    img: bytes | None
    price: float | None
    description: str | None
    link_url: HttpUrl | None
    is_priority: bool | None
    
