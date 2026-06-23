from fastapi import APIRouter

router = APIRouter(
    prefix="users",
    tags=["users"]
)

@router.post("sign-up")
async def sign_up_r():
    pass