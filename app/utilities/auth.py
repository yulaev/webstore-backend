from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from app.models import UserRole
from jwt.exceptions import InvalidTokenError

load_dotenv()

HASHING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/sign-in")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: str
    role: UserRole


def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user):
    if not user:
        return False
    pw = user.password_hash
    if not bcrypt.checkpw(form_data.password.encode("utf-8"), pw.encode("utf-8")):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire_date = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire_date})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


def get_access_token(user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name, "role": user.role}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")

def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        return payload
    except InvalidTokenError:
        raise credentials_exception
    