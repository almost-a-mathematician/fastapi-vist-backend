import asyncio
from database import Session
from api.wishlist.models import Wishlist, wishlist_users_association
from api.user.models import User
from sqlalchemy import select
from api.gift.models import Gift


class WishlistService:
   
    def _filter_visible_for(self, query, user: User):
        query = query.where(
            # WHERE (wishlist.archived_at != NULL) OR (wishlist.owner_id = 123)
            (Wishlist.archived_at == None) | (Wishlist.owner_id == user.id) # перегрузка оператора 
        ).where(
            ~Wishlist.users.any() | Wishlist.users.any(wishlist_users_association.user_id == user.id)
        ) 
        return query
    
    async def _load_gifts_for_wishlist(self, session, wishlist: Wishlist, max = 4):
        gifts_query = select(Gift).where(Gift.wishlist_id == wishlist.id).limit(max)

        gifts = (await session.scalars(gifts_query)).all()

        wishlist.gifts = gifts

        return wishlist

    async def get(self, user: User, owner_id: int):
        async with Session() as session:  

            query = select(Wishlist).where(Wishlist.owner_id == owner_id).where(Wishlist.archived_at == None)
                
            query = self._filter_visible_for(query, user)

            wishlists = (await session.scalars(query)).all()

            corutine_objects = [self._load_gifts_for_wishlist(session, wishlist) for wishlist in wishlists]
            await asyncio.gather(*corutine_objects)

            return wishlists
        
    async def get_archived(self, user: User):
        async with Session() as session:
            
            query = select(Wishlist).where(Wishlist.owner_id == user.id).where(Wishlist.archived_at != None)

            wishlists = (await session.scalars(query)).all()

            corutine_objects = [self._load_gifts_for_wishlist(session, wishlist) for wishlist in wishlists]
            await asyncio.gather(*corutine_objects)
          
            return wishlists
        
        
wishlist_service = WishlistService()