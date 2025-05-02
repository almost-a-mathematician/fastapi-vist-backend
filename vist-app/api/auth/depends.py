from fastapi import Depends, Header, HTTPException
from jwt import ExpiredSignatureError
from api.auth.services.token_manager import access_token
from api.user.services import user_service


async def get_user_by_token(authorization = Header()):
    type, token = authorization.split(' ')

    try:
        jwt_claims = access_token.verify(token)
        return await user_service.get(id=jwt_claims.sub)
    except ExpiredSignatureError:
        raise HTTPException(status_code=403)
    except:
        raise HTTPException(status_code=401)

AuthUserDep = Depends(get_user_by_token)

