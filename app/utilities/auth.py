from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from models import UserRole

load_dotenv()

HASHING_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("SECRET_KEY")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    role: UserRole


def authenticate_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user):
    if not user:
        return False
    if not bcrypt.checkpw(form_data.password, user.password_hash):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire_date = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"expire": expire_date})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"username": user.name, "role": user.role}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")