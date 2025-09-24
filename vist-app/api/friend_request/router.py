from fastapi import APIRouter
from api.friend_request.endpoints import init_endpoints


router = APIRouter(
    prefix='/friend_requests',
    tags=['Friend Requests']
)

init_endpoints(router)