from fastapi import APIRouter, HTTPException, UploadFile, Body
from fastapi.responses import JSONResponse
from api.gift.schemas import UpdateGift, СreateGift, GiftFullResponse, BookGift, GiftsFullResponse

from api.auth.depends import AuthUserDep
from api.gift.services.db import gift_service, WishlistIsNotExistException, WishlistPermissionException, GiftIsNotExistException, GiftPermissionException


def init_endpoints(gift_router: APIRouter):

    @gift_router.get('/gifts/booked')
    async def get_booked(user: AuthUserDep, cursor: int = None, limit: int = 24) -> GiftsFullResponse:
        gifts = await gift_service.get_booked(user, cursor, limit)

        return JSONResponse(
            GiftsFullResponse.model_validate({'items': gifts}, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

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

    @gift_router.post(
            path='/gifts/{id}/image',
            responses={
                404: {'description': 'in case if gift does not exist'},
                403: {'description': 'in case if updater has no permission for his action'} 
        }
    )
    async def set_img(id: int, user: AuthUserDep, image: UploadFile):
        try:
            gift = await gift_service.update(id, user, img=image)
        except GiftIsNotExistException:
            raise HTTPException(status_code=404)
        except(WishlistPermissionException, GiftPermissionException):
            raise HTTPException(status_code=403)

        return JSONResponse(
            GiftFullResponse
            .model_validate(gift, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

    
    @gift_router.delete(
        path='/gifts/{id}/image',
        responses={
            404: {'description': 'in case if gift does not exist'},
            403: {'description': 'in case if updater has no permission for his action'} 
        }
    )
    async def delete_img(id: int, user: AuthUserDep):
        try:
            await gift_service.update(id, user, img=None)
        except GiftIsNotExistException:
            raise HTTPException(status_code=404)
        except(WishlistPermissionException, GiftPermissionException):
            raise HTTPException(status_code=403)
        
        return True


    @gift_router.put(
            path='/gifts/{id}/book',
            responses={
                404: {'description': 'in case if gift does not exist'},
                403: {'description': 'in case if booker has no permission for his action'} 
        }
    )
    async def book(id: int, payload: BookGift, user: AuthUserDep):
        try:
            gift = await gift_service.book(id, payload.booked_by, user)
        except GiftIsNotExistException:
            raise HTTPException(status_code=404)
        except (GiftPermissionException, WishlistPermissionException):
            raise HTTPException(status_code=403)
       
        return JSONResponse(
           GiftFullResponse.model_validate(gift, from_attributes=True)
           .model_dump(context={'auth_user_id': user.id})
        )
    
    @gift_router.patch(
            path='/gifts/{id}',
            responses={
                404: {'description': 'in case if gift does not exist'},
                403: {'description': 'in case if user has no permission for his action'} 
        }
    )
    async def update(id: int, user: AuthUserDep, payload: UpdateGift):
        try:
            gift = await gift_service.update(id, user,  **payload.model_dump(exclude_unset=True))
        except GiftIsNotExistException:
            raise HTTPException(status_code=404)
        except (GiftPermissionException, WishlistPermissionException):
            raise HTTPException(status_code=403)
        
        return JSONResponse(
            GiftFullResponse.model_validate(gift, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )
       
    @gift_router.delete(
            path='/gifts/{id}',
            responses={
                404: {'description': 'in case if gift does not exist'},
                403: {'description': 'in case if user has no permission for his action'} 
        }
    )
    async def delete(id: int, user: AuthUserDep):
        try:
            await gift_service.delete(id, user)
        except GiftIsNotExistException:
            raise HTTPException(status_code=404)
        except (GiftPermissionException, WishlistPermissionException):
            raise HTTPException(status_code=403)

        return True

