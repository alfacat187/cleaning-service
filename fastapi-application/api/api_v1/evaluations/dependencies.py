from typing import Annotated
from uuid import UUID

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.api_v1.offers.schemas import UserInfo
from crud.evaluations import evaluations_crud


async def get_cleaner_by_id_from_path(
    cleaner_id: Annotated[UUID, Path()],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserInfo:
    if cleaner := await evaluations_crud.get_cleaner_info(
        session=session,
        user_id=cleaner_id,
    ):
        return cleaner

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cleaning specialist not found",
    )
