from typing import (
    Annotated,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    UUID4,
    AfterValidator,
)

from api.api_v1.offers.schemas import UserInfo
from api.api_v1.cleanings.schemas import CleaningPublic
from utils.pagination.schemas import (
    SortBy,
    ItemQueryParams,
)


def round_to(ndigits: int) -> AfterValidator:
    return AfterValidator(lambda v: round(v, ndigits))


class CleanerInfo(UserInfo):
    user_id: UUID4


class EvaluationBase(BaseModel):
    no_show: bool = False
    headline: Annotated[str, Field(max_length=150)] | None
    comment: str | None
    professionalism: Annotated[int, Field(strict=True, ge=0, le=5)] | None
    completeness: Annotated[int, Field(strict=True, ge=0, le=5)] | None
    efficiency: Annotated[int, Field(strict=True, ge=0, le=5)] | None
    overall_rating: Annotated[int, Field(strict=True, ge=0, le=5)]


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationInDB(EvaluationBase):
    owner: UUID4
    cleaner_id: UUID4


class EvaluationPublic(EvaluationInDB):
    id: int


class EvaluationAggregate(BaseModel):
    cleaner: CleanerInfo
    avg_professionalism: Annotated[float, round_to(2)]
    avg_completeness: Annotated[float, round_to(2)]
    avg_efficiency: Annotated[float, round_to(2)]
    avg_overall_rating: Annotated[float, round_to(2)]
    max_overall_rating: int
    min_overall_rating: int
    one_stars: int
    two_stars: int
    three_stars: int
    four_stars: int
    five_stars: int
    total_evaluations: int
    total_no_show: int


class SortByEvaluation(SortBy):
    id = "id"
    overall_rating = "overall_rating"


class ItemParamsEvaluation(ItemQueryParams):
    sort_by: SortByEvaluation | None = None
