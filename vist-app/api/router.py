from fastapi import APIRouter
from api.wishlist.router import router as wishlist_router
from api.search.router import router as search_router
from api.friend_request.router import router as friend_request_router
from api.gift.router import router as gift_router
from api.user.router import router as user_router
from api.auth.router import router as auth_router


router = APIRouter(prefix='')
router.include_router(wishlist_router)
router.include_router(search_router)
router.include_router(friend_request_router)
router.include_router(gift_router)
router.include_router(user_router)
router.include_router(auth_router)


