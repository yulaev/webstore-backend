from database import get_session
from pydantic import BaseModel

class User(BaseModel):
    pass

def sign_up():
    with get_session() as session:
        pass