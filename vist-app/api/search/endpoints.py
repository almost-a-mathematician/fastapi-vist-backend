from fastapi import APIRouter
from api.auth.depends import AuthUserDep
from api.search.schemas import SearchResponse
from fastapi.responses import JSONResponse
from api.search.services.db import search_service


def init_endpoints(search_router: APIRouter):

    @search_router.get('/')
    async def search(search: str, user: AuthUserDep) -> SearchResponse:
        search_result = await search_service.search(search, user)

        return JSONResponse(
           SearchResponse.model_validate(search_result, from_attributes=True)
           .model_dump(context={'auth_user_id': user.id})
        )
    
