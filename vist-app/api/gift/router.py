from fastapi import APIRouter
from api.gift.endpoints import init_endpoints
import api.gift.events

router = APIRouter(tags=['Gifts'])

init_endpoints(router)
