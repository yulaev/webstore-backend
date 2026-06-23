from pydantic import BaseModel
from models import UserRole

class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    role: UserRole.customer

class UserPublic(BaseModel):
    name: str
    email: str
    role: UserRole

class UserPrivate(UserPublic):
    password_hash: str