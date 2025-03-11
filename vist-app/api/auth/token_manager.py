from jwt import decode, encode
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv() # оплучаем доступ к переменным .env


class TokenManager:

    # secret = None
    # lifetime = None

    def __init__(self, secret, lifetime):
        self.secret = secret
        self.lifetime = lifetime

    def verify(self, token):
        return decode(token, self.secret)

    def create(self, id):
       return encode({'sub': id, 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=self.lifetime)}, self.secret)


email_token = TokenManager(os.getenv('EMAIL_TOKEN_SECRET'), int(os.getenv('EMAIL_TOKEN_LIFETIME')))
access_token = TokenManager(os.getenv('ACCESS_TOKEN_SECRET'), int(os.getenv('ACCESS_TOKEN_LIFETIME')))
refresh_token = TokenManager(os.getenv('REFRESH_TOKEN_SECRET'), int(os.getenv('REFRESH_TOKEN_LIFETIME')))
