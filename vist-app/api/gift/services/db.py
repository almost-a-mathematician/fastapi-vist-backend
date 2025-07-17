from api.user.models import User
from database import Session
from api.gift.models import Gift
from api.wishlist.services.db import wishlist_service, WishlistIsNotExistException, WishlistPermissionException
from api.wishlist.models import Wishlist


class GiftService:

    async def create(self, wishlist_id, name: str, price: float, description: str, link_url: str, is_priority: bool, user: User):
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

        
gift_service = GiftService()
