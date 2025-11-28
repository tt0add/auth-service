import jwt
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime


load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()

    expires = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({'exp': expires, 'type': 'access'})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt

def create_refresh_token(data: dict, expire_days: int = REFRESH_TOKEN_EXPIRE_DAYS):
    to_encode = data.copy()

    expires = datetime.utcnow() + timedelta(days=expire_days)
    to_encode.update({'exp': expires, 'type': 'refresh'})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt

def decode_jwt(token: str):

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise
