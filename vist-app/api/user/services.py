from database import Session
from api.user.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class UserExistsException(BaseException): 
    ...

class UserIsNotExistException(BaseException): 
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
        
    async def update(self, id, **kwargs):
        async with Session() as session:
            user = await session.get(User, id)
            if user == None:
                raise UserIsNotExistException
            
            for key, value in kwargs:
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()

            return user

    async def get(self, **kwargs):
        async with Session() as session:
            query = select(User)

            for key, value in kwargs:
                if hasattr(User, key):
                    column = getattr(User, key)
                    query = query.where(column == value)

            user = (await session.scalars(query)).first()

            if user == None:
                raise UserIsNotExistException
    
            return user

            
user_service = UserService()