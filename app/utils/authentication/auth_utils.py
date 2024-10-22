from datetime import timedelta, datetime, timezone
from typing import Union, Any

from passlib.context import CryptContext

from app.config import get_settings
from jose import jwt


class JWTAuthUtils:
    def __init__(self):
        self._ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        self._REFRESH_TOKEN_EXPIRE_MINUTES = get_settings().REFRESH_TOKEN_EXPIRE_MINUTES
        self._ALGORITHM = get_settings().ALGORITHM
        self._JWT_SECRET_KEY = get_settings().JWT_SECRET_KEY
        self._JWT_REFRESH_SECRET_KEY = get_settings().JWT_REFRESH_SECRET_KEY
        self._PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_hashed_password(self, password: str) -> str:
        return self._PASSWORD_CONTEXT.hash(password)

    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return self._PASSWORD_CONTEXT.verify(password, hashed_pass)

    def get_expires_delta(self, expires_delta: int = None):
        # Define GMT+5 timezone
        gmt_plus_5 = timezone(timedelta(hours=5))
        if expires_delta is not None:
            # Convert expires_delta from int (minutes or seconds) to timedelta
            time_delta = timedelta(minutes=expires_delta)
        else:
            # Default expiration time if expires_delta is None
            time_delta = timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES)

        expires_delta = datetime.now(gmt_plus_5) + time_delta
        return expires_delta

    def create_access_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        expires_delta = self.get_expires_delta(expires_delta=expires_delta)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self._JWT_SECRET_KEY, self._ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, subject: Union[str, Any], expires_delta: int = None) -> str:
        expires_delta = self.get_expires_delta(expires_delta=expires_delta)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self._JWT_REFRESH_SECRET_KEY, self._ALGORITHM)
        return encoded_jwt
