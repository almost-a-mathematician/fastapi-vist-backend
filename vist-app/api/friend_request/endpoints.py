from fastapi import APIRouter


def init_endpoints(friend_request_router: APIRouter):
    @friend_request_router.get('/privet')
    async def pivet():
        return 'lalala'