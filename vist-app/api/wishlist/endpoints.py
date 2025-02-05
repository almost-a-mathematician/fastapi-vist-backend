from fastapi import APIRouter


def init_endpoints(wishlist_router: APIRouter):

    @wishlist_router.get('/pivet')
    async def pivet():
        print('пивет йа перви индпоинт тута!')
        return 'lalala'





