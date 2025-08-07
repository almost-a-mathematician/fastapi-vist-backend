from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.auth.depends import AuthUserDep
from api.user.schemas import UserResponse
from api.user.services.db import user_service, UserIsNotExistException


def init_endpoints(user_router: APIRouter):

    @user_router.get('/{id}')
    async def get(id: int, user: AuthUserDep) -> UserResponse:
        try:
            found_user = await user_service.get(id=id)
        except UserIsNotExistException:
            raise HTTPException(status_code=404)
        
        return JSONResponse(
            UserResponse
            .model_validate(found_user, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

        
        