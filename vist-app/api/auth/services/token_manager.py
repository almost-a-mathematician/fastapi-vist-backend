from jwt import decode, encode
from datetime import datetime, timedelta, timezone
import os


class TokenManager:

    def __init__(self, secret, lifetime):
        self.secret = secret
        self.lifetime = lifetime

    def verify(self, token):
        return decode(token, self.secret, algorithms=('HS256'))

    def create(self, id, lifetime: int | None = None):
       if lifetime is None:
           lifetime = self.lifetime
       return encode({'sub': str(id), 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=lifetime)}, self.secret, algorithm='HS256')


email_token = TokenManager(
    secret=os.getenv('EMAIL_TOKEN_SECRET'), 
    lifetime=int(os.getenv('EMAIL_TOKEN_LIFETIME'))
)

access_token = TokenManager(
    secret=os.getenv('ACCESS_TOKEN_SECRET'), 
    lifetime=int(os.getenv('ACCESS_TOKEN_LIFETIME'))
)

refresh_token = TokenManager(
    secret=os.getenv('REFRESH_TOKEN_SECRET'), 
    lifetime=int(os.getenv('REFRESH_TOKEN_LIFETIME'))
)



