from fastapi import APIRouter
from api.wishlist.endpoints import init_endpoints


router = APIRouter(
    prefix='/wishlists', 
    tags=['Wishlists']
)

init_endpoints(router)
