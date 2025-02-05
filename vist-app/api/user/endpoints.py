from fastapi import APIRouter


def init_endpoints(user_router: APIRouter):

    @user_router.get('/lalala')
    async def lalala():
        return 'lalala'