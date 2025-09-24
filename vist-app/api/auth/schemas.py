from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, model_validator
from api.user.schemas import UserSerializer


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str

class Login(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str

    @model_validator(mode='after')
    def check_username_or_email_filled(self):
        if (self.username is None) == (self.email is None):
            raise ValueError
        
        return self
    
class ForgetPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    password: str

class RegisterSerializer(BaseModel):
    user: UserSerializer
    avatar_token: str

class DuplicateUserSerializer(BaseModel):
    column: Literal['email', 'username'] 

class TokensSerializer(BaseModel):
    access: str
    refresh: str
    

