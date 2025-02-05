from fastapi import APIRouter


def init_endpoints(gift_router: APIRouter):

    @gift_router.get('/pivet')
    async def pivet():
        return 'lalala'