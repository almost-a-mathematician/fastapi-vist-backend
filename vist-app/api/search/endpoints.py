from fastapi import APIRouter, Request
from api.auth.depends import AuthUserDep
from api.search.schemas import SearchResponse
from fastapi.responses import JSONResponse
from api.search.services.db import search_service
from cache import cache_manager
import json

def init_endpoints(search_router: APIRouter):

    @search_router.get('/')
    async def search(search: str, user: AuthUserDep, request: Request) -> SearchResponse:
        cache_key = request.url.path + request.url.query

        cache = await cache_manager.get(cache_key)

        if cache is not None:
            dumped_model = cache
            print("from cache")
        else:
            search_result = await search_service.search(search, user)

            dumped_model = (
                SearchResponse.model_validate(search_result, from_attributes=True)
               .model_dump_json(context={'auth_user_id': user.id})
            )

            await cache_manager.set(cache_key, dumped_model, 60)
            print("from db")
        
        return JSONResponse(json.loads(dumped_model))
    
