from fastapi import APIRouter
from api.gift.endpoints import init_endpoints


router = APIRouter(tags=['Gifts'])

init_endpoints(router)