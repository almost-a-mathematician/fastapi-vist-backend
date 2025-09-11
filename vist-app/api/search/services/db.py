from sqlalchemy import select
from database import Session, AsyncSessionMaker
from api.user.models import User
from api.wishlist.models import Wishlist
from api.wishlist.services.db import WishlistService, wishlist_service
from sqlalchemy.orm import selectinload
from sqlalchemy import func, text

class SearchService:
    def __init__(self, Session: AsyncSessionMaker, wishlist_service: WishlistService):
        self.Session = Session
        self.wishlist_service = wishlist_service

    async def search(self, search: str, user: User):
        async with self.Session() as session:
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch SCHEMA public")) # levenshtein
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm SCHEMA public")) # similarity

            user_query = (
                select(User)
                .where(func.similarity(User.username, search) > 0.01)
                .order_by(func.levenshtein(User.username, search))
                .limit(10)
            )
            
            wishlist_query = (
                select(Wishlist)
                .where(func.similarity(User.username, search) > 0.01)
                .order_by(func.levenshtein(Wishlist.name, search))
                .options(selectinload(Wishlist.users), selectinload(Wishlist.gifts))
                .limit(20)
            )

            wishlist_query = self.wishlist_service.filter_visible_for(wishlist_query, user) 

            users = (await session.scalars(user_query)).all()
            wishlists = (await session.scalars(wishlist_query)).all()
            
            return {'users': users, 'wishlists': wishlists}

search_service = SearchService(Session, wishlist_service)