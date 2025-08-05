from typing import List
from database import AsyncSessionMaker, Session
from api.wishlist.models import Wishlist
from api.user.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from api.user.models import user_friend_association

class WishlistIsNotExistException(BaseException):
    ...

class WishlistPermissionException(BaseException):
    ...
class WishlistService:
    def __init__(self, Session: AsyncSessionMaker):
        self.Session = Session
   
    def filter_visible_for(self, query, user: User):
        query = query.where(
            # WHERE (wishlist.archived_at != NULL) OR (wishlist.owner_id = 123)
            (Wishlist.archived_at == None) | (Wishlist.owner_id == user.id) # перегрузка оператора 
        ).where(
            ~Wishlist.users.any() | Wishlist.users.any(User.id == user.id)
        ) 
        return query

    async def get(self, user: User, owner_id: int, cursor: int | None, limit: int): 
        async with self.Session() as session:    

            query = (
                select(Wishlist)
                .where(Wishlist.owner_id == owner_id)
                .where(Wishlist.archived_at == None)
                .options(selectinload(Wishlist.users), selectinload(Wishlist.gifts))   
                .order_by(Wishlist.id)
                .limit(limit)
            )
            
            if cursor:
                query = query.where(Wishlist.id > cursor)
                
            query = self.filter_visible_for(query, user)

            wishlists = (await session.scalars(query)).all()

            return wishlists
        
    async def get_archived(self, user: User, cursor: int | None, limit: int):
        async with self.Session() as session:
            
            query = (
                select(Wishlist)
                .where(Wishlist.owner_id == user.id)
                .where(Wishlist.archived_at != None)
                .options(selectinload(Wishlist.users), selectinload(Wishlist.gifts))   
                .order_by(Wishlist.id)
                .limit(limit)
            )
                
            if cursor:
                query = query.where(Wishlist.id > cursor)

            query = self.filter_visible_for(query, user)

            wishlists = (await session.scalars(query)).all()
          
            return wishlists
    
    async def get_by_friends(self, user: User, cursor: int | None, limit: int):
        async with self.Session() as session:

            query = (
                select(Wishlist)
                .join(User, Wishlist.owner_id == User.id)
                .join(
                    user_friend_association, 
                    User.id == user_friend_association.c.friend_id
                )
                .where(user_friend_association.c.user_id == user.id)
                .options(selectinload(Wishlist.users), selectinload(Wishlist.gifts))
                .order_by(Wishlist.id)
                .limit(limit)
            )

            if cursor:
                query = query.where(Wishlist.id > cursor)

            query = self.filter_visible_for(query, user)
        
            wishlists = (await session.scalars(query)).all()
        
            return wishlists
        
    async def get_by_id(self, id, user: User):
        async with self.Session() as session:

            query = select(Wishlist).where(Wishlist.id == id).options(selectinload(Wishlist.owner).selectinload(User.friends))
            query = self.filter_visible_for(query, user)

            wishlist = (await session.scalars(query)).first()

            return wishlist
        
    async def create(self, owner: User, name: str, archived_at=None):
        async with self.Session() as session:

            wishlist = Wishlist(
                name=name, 
                owner=owner, 
                archived_at=archived_at, 
                users=[owner], 
                gifts=[]
            )   

            session.add(wishlist)
            await session.commit()
            await session.refresh(wishlist, attribute_names=Wishlist.get_all_columns())
            
            return wishlist
        
    async def update(self, id, updater: User, **kwargs):
        async with self.Session() as session:
            wishlist = await session.get(Wishlist, id, options=[selectinload(Wishlist.users), selectinload(Wishlist.gifts)])

            if wishlist == None:
                raise WishlistIsNotExistException
            
            if wishlist.owner_id != updater.id:
                raise WishlistPermissionException
            
            for key, value in kwargs.items():
                if hasattr(wishlist, key):
                    setattr(wishlist, key, value)

            await session.commit()
            await session.refresh(wishlist, attribute_names=Wishlist.get_all_columns())
            
            return wishlist
        
    async def update_users(self, id, updater: User, user_list: List[int]):
        async with self.Session() as session:
            wishlist = await session.get(Wishlist, id, options=[selectinload(Wishlist.users)])
        
            if wishlist is None:
                raise WishlistIsNotExistException

            if wishlist.owner_id != updater.id:
                raise WishlistPermissionException

            query = select(User).where(User.id.in_(user_list))
            users = (await session.scalars(query)).all()

            wishlist.users = users

            await session.commit()
            await session.refresh(wishlist, attribute_names=Wishlist.get_all_columns())
        
            return wishlist 

        
wishlist_service = WishlistService(Session)