from fastapi import APIRouter
from api.gift.endpoints import init_endpoints


router = APIRouter(
    prefix='/gifts', 
    tags=['Gifts']
)

init_endpoints(router)