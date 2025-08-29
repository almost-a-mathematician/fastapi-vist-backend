from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.auth.depends import AuthUserDep
from api.media.services.media import media_service


def init_endpoints(media_router: APIRouter):

    @media_router.get(
        path='/{id}',
        responses={
            404: {'description': 'in case if img does not exist'}
        }
    )
    async def get(id: str) -> StreamingResponse:
        download_generator = await media_service.streaming_download(id)
        if download_generator is None:
            raise HTTPException(status_code=404)

        return StreamingResponse(download_generator)


    
    