from typing import (
    Annotated,
    Any,
)

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join

from api.api_v1.evaluations.schemas import (
    EvaluationPublic,
    EvaluationCreate,
    EvaluationInDB,
    ItemParamsEvaluation,
    CleanerInfo,
    EvaluationAggregate,
)
from auth.schemas import UserAuthSchema
from auth.dependencies import UserProfilePermissionGetter
from api.api_v1.cleanings.models import Cleaning
from api.api_v1.cleanings.dependencies import get_one_cleaning
from api.api_v1.evaluations.dependencies import get_cleaner_by_id_from_path
from core.models import db_helper
from crud.evaluations import evaluations_crud
from api.api_v1.cleanings.schemas import CleaningPublic


#
from api.api_v1.evaluations.models import CleanerEvaluation
from uuid import uuid4
import random

#
from utils.pagination.schemas import PaginatedResponse
from utils.pagination.paginator import paginate
from api.api_v1.evaluations.models import CleanerEvaluation

router = APIRouter(
    tags=["Evaluations"],
)


@router.post(
    "/{cleaner_id}",
    response_model=EvaluationPublic,
    status_code=status.HTTP_201_CREATED,
    name="evaluations:create-evaluation-for-cleaner",
    summary="creating an evaluation for the cleaner",
)
async def create_evaluation_for_cleaner(
    user_auth: Annotated[
        UserAuthSchema, Depends(UserProfilePermissionGetter("customer"))
    ],
    cleaner: Annotated[CleanerInfo, Depends(get_cleaner_by_id_from_path)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    evaluation: EvaluationCreate,
) -> EvaluationPublic:
    evaluation_in_db = EvaluationInDB(
        owner=user_auth.id, cleaner_id=cleaner.user_id, **evaluation.model_dump()
    )
    if created_evaluation := await evaluations_crud.create_evaluation(
        session=session,
        evaluation=evaluation_in_db,
    ):
        return created_evaluation

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You've already evaluated this cleaning specialist",
    )


@router.get(
    "/all",
    response_model=PaginatedResponse[EvaluationPublic],
    name="show-all-evaluations-about-cleaners",
    summary="show all evaluations for cleaning specialists",
)
async def show_all_evaluations_about_cleaners(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    params: ItemParamsEvaluation = Depends(),
    max_results: int = Query(default=100, ge=1, le=100),
    cursor: str = Query(None),
) -> dict[str, Any]:

    return await paginate(
        session=session,
        model=CleanerEvaluation,
        query=select(CleanerEvaluation),
        max_results=max_results,
        cursor=cursor,
        params=params,
    )


@router.get(
    "/{cleaner_id}",
    response_model=list[EvaluationPublic],
    name="evaluations:show-all-evaluations-for-cleaner",
    summary="show all evaluations for the cleaner",
)
async def show_all_evaluations_for_cleaner(
    cleaner: Annotated[CleanerInfo, Depends(get_cleaner_by_id_from_path)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[EvaluationPublic]:
    evaluations = await evaluations_crud.get_all_cleaner_evaluations(
        session=session,
        cleaner=cleaner,
    )

    return evaluations


# @router.get(
#     "/{cleaning_id}",
#     response_model=EvaluationPublic,
#     name="evaluations:show-evaluation-info-by-cleaning-id",
# )
# async def show_evaluation_info_by_cleaning_id():
#     pass


@router.get(
    "/{cleaner_id}/stats",
    response_model=EvaluationAggregate,
    name="evaluations:show-stats-about-cleaner",
    summary="show stats about the cleaner",
)
async def show_stats_about_cleaner(
    cleaner: Annotated[CleanerInfo, Depends(get_cleaner_by_id_from_path)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> EvaluationAggregate:
    evaluation_aggregate = await evaluations_crud.get_cleaner_aggregates(
        session=session,
        cleaner=cleaner,
    )

    return evaluation_aggregate


@router.post(
    "/{cleaning_id}/create-eval",
)
async def create_evaluation_for_cleaner_22(
    cleaning: Annotated[Cleaning, Depends(get_one_cleaning)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    for x in range(1, 35):
        session.add(
            CleanerEvaluation(
                owner=uuid4(),
                cleaner_id=cleaning.owner,
                no_show=False,
                headline="string",
                comment=f"its comment {x}",
                professionalism=random.randint(1, 5),
                completeness=random.randint(1, 5),
                efficiency=random.randint(1, 5),
                overall_rating=random.randint(1, 5),
            )
        )
        await session.commit()

    return {"mes": "created"}
