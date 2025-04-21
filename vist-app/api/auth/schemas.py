from pydantic import BaseModel, EmailStr


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str

class VerifyResponse(BaseModel):
    access: str
    refresh: str