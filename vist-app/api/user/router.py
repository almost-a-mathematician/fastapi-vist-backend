from fastapi import APIRouter
from api.user.endpoints import init_endpoints
import api.user.events

router = APIRouter(prefix='/users', tags=['Users'])

init_endpoints(router)
