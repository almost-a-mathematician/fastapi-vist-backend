from sqlalchemy import select
from api.user.models import User
from database import Session, AsyncSessionMaker
from api.gift.models import Gift
from api.wishlist.services.db import WishlistService, wishlist_service, WishlistIsNotExistException, WishlistPermissionException
from api.wishlist.models import Wishlist
from sqlalchemy.orm import selectinload


class GiftIsNotExistException(BaseException):
    ...

class GiftPermissionException(BaseException):
    ...

class GiftService:
    def __init__(self, Session: AsyncSessionMaker, wishlist_service: WishlistService):
        self.Session = Session
        self.wishlist_service = wishlist_service

    async def get_booked(self, user: User, cursor: int | None, limit: int):
        async with self.Session() as session:
            
            query = (
                select(Gift)
                .where(Gift.booked_by_id == user.id)
                .join(Wishlist, Gift.wishlist_id == Wishlist.id)
                .limit(limit)
                .options(selectinload(Gift.booked_by))
            )

            query = self.wishlist_service.filter_visible_for(query, user)

            if cursor:
                query = query.where(Gift.id > cursor)

            gifts = (await session.scalars(query)).all()

            return gifts

    async def create(
        self, 
        wishlist_id, 
        name: str, 
        price: float, 
        description: str, 
        link_url: str, 
        is_priority: bool, 
        user: User
    ):
        async with self.Session() as session:
            
            wishlist = await session.get(Wishlist, wishlist_id)

            if wishlist == None:
                raise WishlistIsNotExistException
            if wishlist.owner_id != user.id:
                raise WishlistPermissionException

            gift = Gift(
                name=name, 
                price=price, 
                description=description, 
                link_url=link_url,
                is_priority=is_priority, 
                wishlist=wishlist
            )

        session.add(gift)
        await session.commit()
        await session.refresh(gift)

        return gift
    
    async def update(self, id, user: User, **kwargs):
        async with self.Session() as session:

            gift = await session.get(Gift, id)

            if gift == None:
                raise GiftIsNotExistException
            
            wishlist = await self.wishlist_service.get_by_id(gift.wishlist_id, user)

            if wishlist == None:
                raise WishlistPermissionException

            if user.id != wishlist.owner_id:
                raise GiftPermissionException
            
            for key, value in kwargs.items():
                if hasattr(gift, key):
                    setattr(gift, key, value)

            await session.commit()
            await session.refresh(gift, attribute_names=Gift.get_all_columns())

            return gift
            

    async def book(self, id, booked_by: int | None, user: User):
        async with self.Session() as session:

            gift = await session.get(Gift, id, options=[selectinload(Gift.booked_by)])

            if gift == None:
                raise GiftIsNotExistException

            wishlist = await self.wishlist_service.get_by_id(gift.wishlist_id, user) 
            
            if wishlist == None or (wishlist.owner_id != user.id and not wishlist.owner.are_friends_with(user)):
                raise WishlistPermissionException

            if booked_by != None:
                if user.id != wishlist.owner_id and gift.booked_by_id != None:
                    raise GiftPermissionException
                
                gift.booked_by_id = user.id
            else:
                if wishlist.owner_id != user.id and gift.booked_by_id != user.id:
                    raise GiftPermissionException

                gift.booked_by_id = None

            session.add(gift)
            await session.commit()
            await session.refresh(gift)

        return gift
    
    async def delete(self, id, user: User):
        async with self.Session() as session:
            
            gift = await session.get(Gift, id)
            
            if gift == None:
                raise GiftIsNotExistException
            
            wishlist = await self.wishlist_service.get_by_id(gift.wishlist_id, user)
            
            if wishlist == None:
                raise WishlistPermissionException
            
            if user.id != wishlist.owner_id:
                raise GiftPermissionException
            
            await session.delete(gift)
            await session.commit()
            
            return True
        
gift_service = GiftService(Session, wishlist_service)
