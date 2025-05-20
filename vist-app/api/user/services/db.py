from asyncpg import UniqueViolationError
from database import Session
from api.user.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

class UserExistsException(BaseException): 
    def __init__(self, column: str):
        self.column = column

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
                await session.refresh(user)
            except IntegrityError as e: 

                original_error = e.__cause__.__cause__

                if isinstance(original_error, UniqueViolationError):
                    raise UserExistsException(column='email' if '(email)' in str(original_error) else 'username')       
                else:
                    raise e
    
            return user
        
    async def update(self, id, **kwargs):
        async with Session() as session:
            user = await session.get(User, id)
            if user == None:
                raise UserIsNotExistException
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            await session.commit()

            return user

    async def get(self, **kwargs):
        async with Session() as session:
            query = select(User)

            for key, value in kwargs.items():
                if hasattr(User, key):
                    column = getattr(User, key)
                    query = query.where(column == value)

            user = (await session.scalars(query)).first()

            if user == None:
                raise UserIsNotExistException
    
            return user

            
user_service = UserService()