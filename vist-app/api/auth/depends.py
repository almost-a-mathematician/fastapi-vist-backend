from typing import Annotated
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, PyJWTError
from api.auth.services.token_manager import access_token
from api.user.services.db import UserDoesNotExistException, user_service
from api.user.models import User

auth_schema = HTTPBearer()


async def get_user_by_token(auth: HTTPAuthorizationCredentials = Depends(auth_schema)):
	token = auth.credentials

	try:
		jwt_claims = access_token.verify(token)
		return await user_service.get(id=int(jwt_claims['sub']))
	except ExpiredSignatureError:
		raise HTTPException(status_code=403)
	except (PyJWTError, UserDoesNotExistException):
		raise HTTPException(status_code=401)


AuthUserDep = Annotated[User, Depends(get_user_by_token)]
