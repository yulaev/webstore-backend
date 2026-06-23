from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from .routers import users_router

app = FastAPI()

app.include_router(users_router)