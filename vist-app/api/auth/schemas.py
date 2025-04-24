from pydantic import BaseModel, EmailStr, model_validator


class Register(BaseModel):
    username: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access: str
    refresh: str

class Login(BaseModel):
    username: str | None
    email: EmailStr | None
    password: str

    @model_validator(mode='after')
    def check_username_or_email_filled(self):
        if (self.username == None) == (self.email == None):
            raise ValueError
        
        return self



