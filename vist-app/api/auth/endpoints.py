from fastapi import APIRouter


def init_endpoints(auth_router: APIRouter):

    @auth_router.get('/pivet')
    async def pivet():
        print('lalala')
        return 'lalala'
