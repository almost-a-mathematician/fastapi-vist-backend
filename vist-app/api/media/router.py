from fastapi import APIRouter
from api.media.endpoints import init_endpoints

router = APIRouter(prefix='/media', tags=['Media'])

init_endpoints(router)
