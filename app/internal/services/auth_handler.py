from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from app.pkg.settings import settings
from app.pkg import models
from app.pkg.models.exceptions import (
    InvalidRefreshToken,
    InvalidScopeToken,
    InvalidToken,
    RefreshTokenExpired,
    TokenExpired,
)


class Auth:
    hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # secret = settings.SECRET_KEY.get_secret_value()

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username):
        exp_access_token_minutes = 30
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=exp_access_token_minutes),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'access_token':
                return payload['sub']
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    def decode_refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                return payload['sub']
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    def encode_refresh_token(self, username):
        exp_refresh_token_hours = 24
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, hours=exp_refresh_token_hours),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                username = payload['sub']

                new_token = self.encode_token(username)
                new_refresh = self.encode_refresh_token(username)

                return models.UserRefreshToken(
                    access_token=new_token,
                    refresh_token=new_refresh
                )
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise RefreshTokenExpired
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken

