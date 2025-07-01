from fastapi import APIRouter, Response
from api.auth.depends import AuthUserDep
from api.wishlist.services.db import wishlist_service
from api.wishlist.schemas import WishlistsSerializer


def init_endpoints(wishlist_router: APIRouter):

    @wishlist_router.get('/')
    async def get(owner: int, user: AuthUserDep) -> WishlistsSerializer:

        wishlists = await wishlist_service.get(user, owner_id=owner)

        return WishlistsSerializer(items=wishlists).model_dump(context={'auth_user_id': user.id})
        

        

