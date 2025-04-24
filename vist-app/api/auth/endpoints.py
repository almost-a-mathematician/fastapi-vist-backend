from fastapi import APIRouter, HTTPException
from api.auth.schemas import Login, Register, TokenResponse
from api.auth.services.password_manager import password_manager
from api.user.services import UserExistsException, UserIsNotExistException, user_service
from api.auth.services.token_manager import email_token, access_token, refresh_token
from api.auth.services.mail_sender import mail_sender
import os
from api.user.schemas import UserFullResponse



def init_endpoints(auth_router: APIRouter):

    @auth_router.post('/register')
    async def register(payload: Register) -> UserFullResponse:
        password_hash = password_manager.generate(payload.password)

        try:
            user = await user_service.create(
                username=payload.username, 
                password=password_hash, 
                email=payload.email
            )
        except UserExistsException:
            raise HTTPException(status_code=409, detail='User with this username or email already exists')
        
        token = email_token.create(id=user.id)

        await mail_sender.create_and_send(
            email=user.email, 
            template_filename='email_verify.html', 
            template_params={
                'username':user.username, 
                'link': os.getenv('FRONTEND_VERIFY_PAGE') + f'?token={token}', 
                'lifetime':email_token.lifetime
            }
        )

        return UserFullResponse(**user.__dict__).model_dump()


    @auth_router.post('/verify')
    async def verify(token) -> TokenResponse:
        jwt_claims = email_token.verify(token)
        access = access_token.create(jwt_claims.sub)
        refresh = refresh_token.create(jwt_claims.sub)
        await user_service.update(id=jwt_claims.sub, verified=True)
        return TokenResponse(access, refresh).model_dump()


    @auth_router.post('/login')
    async def login(payload: Login) -> TokenResponse:
        try:
            user = await user_service.get(**payload.model_dump()) 
        except UserIsNotExistException:
            raise HTTPException(status_code=404)

        if not password_manager.check(payload.password, user.password):
            raise HTTPException(status_code=404)
        
        access = access_token.create(user.id)
        refresh = refresh_token.create(user.id)

        return TokenResponse(access, refresh).model_dump()

        

        

        

        






