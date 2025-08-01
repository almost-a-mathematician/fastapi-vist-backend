from api.user.models import User
from database import Session
from api.gift.models import Gift
from api.wishlist.services.db import wishlist_service, WishlistIsNotExistException, WishlistPermissionException
from api.wishlist.models import Wishlist
from sqlalchemy.orm import selectinload


class GiftIsNotExistException(BaseException):
    ...

class GiftPermissionException(BaseException):
    ...

class GiftService:

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
        async with Session() as session:
            
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
    

    async def book(self, id, booked_by: int | None, user: User):
        async with Session() as session:

            gift = await session.get(Gift, id, options=[selectinload(Gift.wishlist), selectinload(Gift.booked_by)])

            if gift == None:
                raise GiftIsNotExistException

            wishlist = await wishlist_service.get_by_id(gift.wishlist_id, user) 
            
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

            
        
gift_service = GiftService()
