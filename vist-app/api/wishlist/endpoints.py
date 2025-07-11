from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.auth.depends import AuthUserDep
from api.wishlist.services.db import wishlist_service, WishlistPermissionException, WishlistIsNotExistException
from api.wishlist.schemas import WishlistsSerializer, WishlistSerializer, CreateWishlist, UpdateWishlist


def init_endpoints(wishlist_router: APIRouter):

    @wishlist_router.get('/')
    async def get(owner: int, user: AuthUserDep) -> WishlistsSerializer:

        wishlists = await wishlist_service.get(user, owner_id=owner)
    
        return JSONResponse(
            WishlistsSerializer
            .model_validate({'items': wishlists}, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )
    
    @wishlist_router.get('/archived')
    async def get_archived(owner: AuthUserDep) -> WishlistsSerializer:

        wishlists = await wishlist_service.get_archived(owner)

        return JSONResponse(
            WishlistsSerializer
            .model_validate({'items': wishlists}, from_attributes=True)
            .model_dump(context={'auth_user_id': owner.id})
        )


    @wishlist_router.post('/')
    async def create(payload: CreateWishlist, creator: AuthUserDep) -> WishlistSerializer:
        wishlist = await wishlist_service.create(
            name=payload.name, 
            owner=creator, 
            archived_at=payload.archived_at
        )

        return JSONResponse(
            WishlistSerializer
            .model_validate(wishlist, from_attributes=True)
            .model_dump(context={'auth_user_id': creator.id})
        )

        
    @wishlist_router.patch(
        path='/{id}',
        responses={
            404: {'description': 'in case if wishlist does not exist'},
            403: {'description': 'in case if updater is not the owner'} 
        }
    )
    async def update(id: int, payload: UpdateWishlist, updater: AuthUserDep) -> WishlistSerializer:
        try:
            wishlist = await wishlist_service.update(id, updater, **payload.model_dump(exclude_unset=True))
        except WishlistIsNotExistException:
            raise HTTPException(status_code=404)
        except WishlistPermissionException:
            raise HTTPException(status_code=403)

        return JSONResponse(
            WishlistSerializer
            .model_validate(wishlist, from_attributes=True)
            .model_dump(context={'auth_user_id': updater.id})
        )
        




        

