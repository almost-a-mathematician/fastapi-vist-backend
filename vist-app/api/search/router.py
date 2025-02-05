from fastapi import APIRouter
from api.search.endpoints import init_endpoints


router = APIRouter(
    prefix='/search',
    tags=['Wishlists', 'Users']
)

init_endpoints(router)