from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.auth.schemas import Register
from api.auth.services.password_manager import password_manager
from api.user.services import UserExistsException, user_service
from api.auth.services.token_manager import email_token
from api.auth.services.mail_sender import mail_sender
import os



def init_endpoints(auth_router: APIRouter):

    @auth_router.post('/register/')
    async def register(payload: Register):
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

        return user
