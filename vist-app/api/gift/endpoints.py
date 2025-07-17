from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.gift.schemas import СreateGift, GiftFullResponse
from api.auth.depends import AuthUserDep
from api.gift.services.db import gift_service, WishlistIsNotExistException, WishlistPermissionException


def init_endpoints(gift_router: APIRouter):

    @gift_router.post(
        path='/wishlists/{wishlist_id}/gifts',
        responses={
            404: {'description': 'in case if wishlist does not exist'},
            403: {'description': 'in case if updater is not the owner'} 
        }
    )
    async def create(wishlist_id: int, payload: СreateGift, user: AuthUserDep) -> GiftFullResponse:
        try:
            gift = await gift_service.create(
                wishlist_id=wishlist_id, 
                name=payload.name, 
                price=payload.price, 
                description=payload.description, 
                link_url=str(payload.link_url), 
                is_priority=payload.is_priority, 
                user=user
            )
        except WishlistIsNotExistException:
            raise HTTPException(status_code=404)
        except WishlistPermissionException:
            raise HTTPException(status_code=403)
        
        return JSONResponse(
            GiftFullResponse.model_validate(gift, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

