from database import get_session
from schemas import UserCreate
from models import User, UserRole
from utilities import get_access_token, authenticate_user
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt
from typing import Annotated


def sign_up(data: UserCreate):
    with get_session() as session:
        if data.role == UserRole.admin:
            raise HTTPException(status_code=403, detail="You are Forbidden from performing this operation")

        s = bcrypt.gensalt()
        pw = data.password.encode("utf-8")
        pw_hash = bcrypt.hashpw(pw, s)
        
        user = User(
            name = data.name,
            password_hash = pw_hash,
            email = data.email,
            role = data.role
        )

        session.add(user)
        session.commit()

        return user
    
def sing_in(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with get_session() as session:
        user = session.get(User, data.username)
        if not authenticate_user:
            HTTPException(status_code=401, detail="Invalid username or password")
        get_access_token(data, user)