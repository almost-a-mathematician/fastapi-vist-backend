from typing import Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from api.auth.schemas import ForgetPassword, Login, Register, ResetPassword, TokensSerializer, DuplicateUserSerializer, RegisterSerializer
from api.auth.services.password_manager import password_manager
from api.user.services.db import UserExistsException, UserDoesNotExistException, user_service
from api.user.services.user_mail_sender import user_mail_sender, SendDelayException
from api.auth.services.token_manager import email_token, access_token, refresh_token
import os
from shared.fix_exec_time import fix_exec_time


def init_endpoints(auth_router: APIRouter):

    @auth_router.post(
        path='/register',
        responses={
            409: {'model': DuplicateUserSerializer}
        }
    )
    async def register(payload: Register) -> RegisterSerializer:
        password_hash = password_manager.generate(payload.password)

        try:
            user = await user_service.create(
                username=payload.username, 
                password=password_hash, 
                email=payload.email
            )
        except UserExistsException as e:
            return JSONResponse(
                status_code=409, 
                content=DuplicateUserSerializer(column=e.column).model_dump()
            )
        
        token = email_token.create(id=user.id)
        try:
            await user_mail_sender.create_and_send(
                user=user, 
                template_filename='email_verify.html', 
                template_params={
                    'username':user.username, 
                    'link': os.getenv('FRONTEND_VERIFY_PAGE') + f'?token={token}', 
                    'lifetime':email_token.lifetime
                }
            )
        except SendDelayException:
            raise HTTPException(status_code=429)

        return JSONResponse( 
            RegisterSerializer
                .model_validate({'user': user, 'avatar_token': access_token.create(id=user.id, lifetime=1)}, from_attributes=True)
                .model_dump(context={'auth_user_id': user.id})
        )


    @auth_router.post('/verify')
    async def verify(token) -> TokensSerializer:
        try:
            jwt_claims = email_token.verify(token)
        except:
            raise HTTPException(status_code=401)
        access = access_token.create(jwt_claims['sub'])
        refresh = refresh_token.create(jwt_claims['sub'])
        await user_service.update(id=int(jwt_claims['sub']), verified=True)
        return {'access': access, 'refresh': refresh}


    @auth_router.post('/login')
    async def login(payload: Login) -> TokensSerializer:
        try:
            if payload.username is not None:
                user = await user_service.get(username=payload.username) 
            elif payload.email is not None:
                user = await user_service.get(email=payload.email) 
        except UserDoesNotExistException:
            raise HTTPException(status_code=404)
        
        if user.verified != True:
            token = email_token.create(id=user.id)

            try:
                await user_mail_sender.create_and_send(
                    user=user, 
                    template_filename='email_verify.html', 
                    template_params={
                        'username':user.username, 
                        'link': os.getenv('FRONTEND_VERIFY_PAGE') + f'?token={token}', 
                        'lifetime':email_token.lifetime
                    }
                )
            except SendDelayException:
                raise HTTPException(status_code=429)

            raise HTTPException(status_code=401)

        if not password_manager.check(provided_password=payload.password, hashed_password=user.password):
            raise HTTPException(status_code=404)

        access = access_token.create(user.id)
        refresh = refresh_token.create(user.id)

        return {'access': access, 'refresh': refresh}
    

    @auth_router.post('/refresh')
    async def refresh(token) -> TokensSerializer:
        try:
            jwt_claims = refresh_token.verify(token)
        except:
            raise HTTPException(status_code=401)
        
        access = access_token.create(jwt_claims['sub'])
        refresh = refresh_token.create(jwt_claims['sub'])

        return {'access': access, 'refresh': refresh}


    @auth_router.post('/forget-password') 
    @fix_exec_time(time=5)
    async def forget_password(payload: ForgetPassword) -> Literal[True]:
        try:
            user = await user_service.get(email=payload.email) 
        except UserDoesNotExistException:
            return True
        
        token = email_token.create(id=user.id)
        try:
            await user_mail_sender.create_and_send(
                user=user, 
                template_filename='reset_password.html', 
                template_params={
                    'username':user.username, 
                    'link': os.getenv('FRONTEND_RESET_PW_PAGE') + f'?token={token}', 
                    'lifetime':email_token.lifetime
                }
            )
        except SendDelayException:
            raise HTTPException(status_code=429)
        
        return True
        

    @auth_router.patch('/reset-password') # добавить возможность менять пароль даже если юзер не забыл старый
    async def reset_password(token, payload: ResetPassword) -> Literal[True]:
        try:  
            jwt_claims = email_token.verify(token)
        except:
            raise HTTPException(status_code=401)
        
        new_password = password_manager.generate(payload.password)

        await user_service.update(id=int(jwt_claims['sub']), password=new_password)

        return True






