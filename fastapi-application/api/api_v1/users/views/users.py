from typing import Annotated

from fastapi import APIRouter

router = APIRouter(
    tags=["Users"],
)


@router.get("")
async def greeting():
    return {"message": "ok"}


# @router.get("/me")
# async def get_info_about_yourself(
#     user_in: Annotated[UserAuthSchema, Depends(get_current_active_auth_user)],
# ):
#
#     return {
#         "email": user_in.email,
#         "logged_in_at": user_in.logged_in_at,
#     }
