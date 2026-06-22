from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from models import Base

load_dotenv()

url = os.getenv("DATABASE_URL")
engine = create_engine(url)

def db_init():
    Base.metadata.create_all(engine)

def get_session():
    return Session(engine)
