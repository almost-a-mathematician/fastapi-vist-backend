from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from api.auth.depends import AuthUserDep
from api.user.schemas import UserResponse, UpdateUser
from api.user.services.db import DuplicateUsernameException, UserPermissionException, user_service, UserDoesNotExistException
from api.media.services.media import media_service
from api.media.schemas import validate_file


def init_endpoints(user_router: APIRouter):

    @user_router.get(
        path='/{id}',
        responses={
            404: {'description': 'in case if user does not exist'}
        }
    )
    async def get(id: int, user: AuthUserDep) -> UserResponse:
        try:
            found_user = await user_service.get(id=id)
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        
        return JSONResponse(
            UserResponse
            .model_validate(found_user, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )
    
    @user_router.post(
            path='/{id}/avatar',
            responses={
            404: {'description': 'in case if user does not exist'},
            403: {'description': 'in case if user has no permission for the action'}
        }
    )
    async def set_avatar(id: int, user: AuthUserDep, img: UploadFile):

        try:
            user = await user_service.update(id, updater=user, profile_pic=img)
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        except UserPermissionException:
            raise HTTPException(status_code=403)

        return JSONResponse(
            UserResponse
            .model_validate(user, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

    @user_router.delete(
            path='/{id}/avatar',
            responses={
            404: {'description': 'in case if user or avatar does not exist'},
            403: {'description': 'in case if user has no permission for the action'}
        }
    )
    async def delete_avatar(id: int, user: AuthUserDep):
        try:
            await user_service.update(id, updater=user, profile_pic=None)
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        except UserPermissionException:
            raise HTTPException(status_code=403)

        return True


    @user_router.patch(
        path='/{id}',
        responses={
            404: {'description': 'in case if user does not exist'},
            403: {'description': 'in case if user has no permission for the action'}, 
            409: {'desctiption': 'duplicate username'}
        }
    )
    async def update(id: int, updater: AuthUserDep, payload: UpdateUser) -> UserResponse:
        try:
            user = await user_service.update(id, updater, **payload.model_dump(exclude_unset=True))
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        except UserPermissionException:
            raise HTTPException(status_code=403)
        except DuplicateUsernameException:
            raise HTTPException(status_code=409)
        
        return JSONResponse(
            UserResponse
            .model_validate(user, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )
            
    @user_router.delete(
        path='/{id}',
        responses={
            404: {'description': 'in case if user does not exist'},
            403: {'description': 'in case if user has no permission for the action'}, 
        }
    )
    async def delete(id: int, user: AuthUserDep):
        try:
            await user_service.delete(id, user)
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        except UserPermissionException:
            raise HTTPException(status_code=403)
        
        return True


