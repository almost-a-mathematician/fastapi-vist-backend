from fastapi import APIRouter
from api.friend_request.endpoints import init_endpoints


router = APIRouter(
    prefix='/friend_requests',
    tags=['Users']
)

init_endpoints(router)