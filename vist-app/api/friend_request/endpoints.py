from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.auth.depends import AuthUserDep
from api.friend_request.schemas import UpdateRequestStatus, FriendRequestResponse, CreateUserFriend, FriendRequestsResponse
from api.friend_request.services.db import friend_request_service, FriendRequestPermissionException, UserDoesNotExistException, FriendRequestDoesNotExistException


def init_endpoints(friend_request_router: APIRouter):
    @friend_request_router.get('/')
    async def get(user: AuthUserDep) -> FriendRequestsResponse:
        friend_requests = await friend_request_service.get(user)

        return JSONResponse(
            FriendRequestsResponse.model_validate({'items': friend_requests}, from_attributes=True)
            .model_dump(context={'auth_user_id': user.id})
        )

    @friend_request_router.post(
        path='/',
        responses={
            403: {'description': 'in case if user has no permission for the action'},
            404: {'description': 'in case if receiver does not exist'}
        }
    )
    async def create (user: AuthUserDep, payload: CreateUserFriend) -> FriendRequestResponse:
        try:
            friend_request = await friend_request_service.create(payload.receiver_id, user, payload.status)
        except FriendRequestPermissionException:
            raise HTTPException(status_code=403)
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
            
        return JSONResponse(
        FriendRequestResponse.model_validate(friend_request, from_attributes=True)
        .model_dump(context={'auth_user_id': user.id})
        )
            
    @friend_request_router.patch(
        path='/{id}',
        responses={
            403: {'description': 'in case if user has no permission for his action'}
        }
    ) 
    async def update(id: int, user: AuthUserDep, payload: UpdateRequestStatus) -> FriendRequestResponse:
        try:
            friend_request = await friend_request_service.update(id, user, payload.status)
        except FriendRequestPermissionException:
            raise HTTPException(status_code=403)
        
        return JSONResponse(
        FriendRequestResponse.model_validate(friend_request, from_attributes=True)
        .model_dump(context={'auth_user_id': user.id})
        )
    
    @friend_request_router.delete(
        path='/{id}',
        responses={
            403: {'description': 'in case if user has no permission for his action'},
            404: {'description': 'in case if friend request does not exist'}
        }
    )
    async def delete(id: int, user: AuthUserDep):
        try:
            await friend_request_service.delete(id, user)
        except FriendRequestPermissionException:
            raise HTTPException(status_code=403)
        except FriendRequestDoesNotExistException:
            raise HTTPException(status_code=404)
        
        return True



