from fastapi import APIRouter
from api.user.endpoints import init_endpoints


router = APIRouter(
    prefix='/users', 
    tags=['Users']
)

init_endpoints(router)