from datetime import datetime, timedelta
import os
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def check_credentials(username: str, password: str):
    admin_username = os.environ['ADMIN_USERNAME']
    admin_password = os.environ['ADMIN_PASSWORD']

    return username == admin_username and password == admin_password


def generate_access_token(data: dict, expiration_delta: timedelta = timedelta(minutes=120)):
    secret_key = os.environ['ENCRYPTION_SECRET_KEY']
    algorithm = os.environ['ENCRYPTION_ALGORITHM']

    expiration_time = datetime.utcnow() + expiration_delta
    data.update({'exp': expiration_time})
    return jwt.encode(data, secret_key, algorithm)


def validate_access_token(token: str):
    secret_key = os.environ['ENCRYPTION_SECRET_KEY']
    algorithm = os.environ['ENCRYPTION_ALGORITHM']

    try:
        payload = jwt.decode(token, secret_key, algorithm)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication cridentials")
        return True

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access_token")
