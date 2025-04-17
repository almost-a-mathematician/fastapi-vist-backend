from database import Session
from api.user.models import User
from sqlalchemy.exc import IntegrityError

class UserExistsException(BaseException): 
    ...

class UserService:
    ''' инкапсулирует логику работы с бд над моделью юзера '''
    async def create(self, username, password, email):
        async with Session() as session:

            try:
                user = User(username=username, password=password, email=email)    
                session.add(user)
                await session.commit()
            except IntegrityError:  # todo: классифицировать IntegrityError и убедиться, что ошибка из-за дубликата в таблице
                raise UserExistsException
        
            session.refresh(user)
    
            return user

user_service = UserService()

