from database import AsyncSessionMaker, Session
from api.user.models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from shared.errors import is_unique_error
from api.auth.services.password_manager import password_manager
from api.media.services.media import media_service, MediaService
from api.media.schemas import validate_file


class UserExistsException(BaseException): 
    def __init__(self, column: str):
        self.column = column

class UserDoesNotExistException(BaseException): 
    ...

class UserPermissionException(BaseException):
    ...

class DuplicateUsernameException(BaseException):
    ...

class UserService:
    def __init__(self, Session: AsyncSessionMaker, media_service: MediaService):
        self.Session = Session
        self.media_service = media_service

    ''' инкапсулирует логику работы с бд над моделью юзера '''
    async def get(self, **kwargs):
        async with self.Session() as session:
            query = select(User)

            for key, value in kwargs.items():
                if hasattr(User, key):
                    column = getattr(User, key)
                    query = query.where(column == value)

            user = (await session.scalars(query)).first()

            if user is None:
                raise UserDoesNotExistException
    
            return user

    
    async def create(self, username, password, email):
        async with self.Session() as session:

            try:
                user = User(username=username, password=password, email=email)    
                session.add(user)
                await session.commit()
                await session.refresh(user)
            except IntegrityError as e: 
                original_error = is_unique_error(e)

                if original_error is not None:
                    raise UserExistsException(column='email' if '(email)' in str(original_error) else 'username')       
                else:
                    raise e
    
            return user
        
    async def update(self, id: int, updater: User, **kwargs):
        async with self.Session() as session:
            user = await session.get(User, id)

            try:
                if user is None:
                    raise UserDoesNotExistException
                if user.id is not updater.id:
                    raise UserPermissionException
                for key, value in kwargs.items():
                    if key == 'password':
                        value = password_manager.generate(value)
                    if key == 'profile_pic': 
                        if user.profile_pic is not None:
                            await self.media_service.delete(user.profile_pic)

                        if value is not None:
                            validate_file(file=value, max_size=1500000, types=['image/png', 'image/jpeg', 'image/jpg', 'png', 'jpeg', 'jpg'])
                            value = await self.media_service.upload(await value.read())

                    if hasattr(user, key):
                        setattr(user, key, value)

                await session.commit()
                await session.refresh(user)

            except  IntegrityError as e: 
                original_error = is_unique_error(e)

                if original_error is not None:
                    raise DuplicateUsernameException      
                else:
                    raise e
        
            return user
        
    async def delete(self, id: int, deleter: User):
        async with self.Session() as session:
            user = await session.get(User, id)
            if user is None:
                raise UserDoesNotExistException
            if user.id is not deleter.id:
                raise UserPermissionException
            
            from api.gift.models import Gift
            
            await session.execute(
                update(Gift)
                .where(Gift.booked_by_id == id)
                .values(booked_by_id=None)
            )
    
            await session.delete(user)
            await session.commit()
            
user_service = UserService(Session, media_service)