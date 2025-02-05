from fastapi import APIRouter


def init_endpoints(search_router: APIRouter):
    @search_router.get('/lalala/')
    async def lalala(search: str):
        print(f'пивет друк база даных дай нам пажалуста пользуватилий и вишлисти с иминим такии букви как {search}')
        return 'lalala'

