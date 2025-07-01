from datetime import date
from pydantic import BaseModel, EmailStr, field_serializer


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
    is_hidden_bd: bool
    email: EmailStr | None
    # friends

    @field_serializer('email')
    def serialize_email(self, email, info):
        try:
            auth_user_id = info.context.get('auth_user_id')
            if auth_user_id == None:
                raise Exception
            
            return email if auth_user_id == self.id else None
    
        except:
            raise Exception('Context is not defined')
        
    @field_serializer('birth_date')
    def serialize_birth_date(self, birth_date, info):
        try:
            auth_user_id = info.context.get('auth_user_id')
            if auth_user_id == None:
                raise Exception
            
            return birth_date if self.is_hidden_bd == False or auth_user_id == self.id else None
     
        except:
            raise Exception('Context is not defined')
        
    

            
            


