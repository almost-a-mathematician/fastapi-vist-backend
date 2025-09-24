from fastapi import APIRouter
from api.auth.endpoints import init_endpoints

router = APIRouter(prefix='/auth', tags=['Auth'])

init_endpoints(router)
