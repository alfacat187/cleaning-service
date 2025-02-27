from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    and_,
    func,
    cast,
    Integer,
)

from crud.base import CRUDRepository
from api.api_v1.evaluations.schemas import (
    EvaluationInDB,
    EvaluationPublic,
    CleanerInfo,
    EvaluationAggregate,
)
from api.api_v1.evaluations.models import CleanerEvaluation
from api.api_v1.users.models import User
from crud.cleanings import cleanings_crud

GET_CLEANER_AGGREGATE_RATINGS_QUERY = """
    SELECT        
        AVG(professionalism) AS avg_professionalism,
        AVG(completeness)    AS avg_completeness,
        AVG(efficiency)      AS avg_efficiency,
        AVG(overall_rating)  AS avg_overall_rating,
        MIN(overall_rating)  AS min_overall_rating,
        MAX(overall_rating)  AS max_overall_rating,
        COUNT(cleaner_id)   AS total_evaluations,
        SUM(no_show::int)    AS total_no_show,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 1) AS one_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 2) AS two_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 3) AS three_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 4) AS four_stars,
        COUNT(overall_rating) FILTER(WHERE overall_rating = 5) AS five_stars
    FROM cleaner_evaluations
    WHERE cleaner_id = :cleaner_id;
"""


class EvaluationsCRUD(CRUDRepository):  # type: ignore
    @staticmethod
    async def get_evaluation(
        session: AsyncSession,
        owner: UUID,
        cleaner_id: UUID,
    ) -> CleanerEvaluation | None:
        res = await session.scalar(
            select(CleanerEvaluation).where(
                and_(
                    CleanerEvaluation.owner == owner,
                    CleanerEvaluation.cleaner_id == cleaner_id,
                )
            )
        )

        return res

    async def create_evaluation(
        self,
        session: AsyncSession,
        evaluation: EvaluationInDB,
    ) -> EvaluationPublic | None:
        if await self.get_evaluation(
            session=session,
            owner=evaluation.owner,
            cleaner_id=evaluation.cleaner_id,
        ):
            return None

        to_create = await self.create_record(
            session=session,
            obj_in=evaluation,
        )

        return EvaluationPublic(**to_create.as_dict())

    @staticmethod
    async def get_cleaner_info(
        session: AsyncSession, user_id: UUID
    ) -> CleanerInfo | None:
        if res := await session.get(User, user_id):
            cleaner_info = res.profile[0]
            return CleanerInfo(**cleaner_info.as_dict())

        return None

    async def get_all_cleaner_evaluations(
        self,
        session: AsyncSession,
        cleaner: CleanerInfo,
    ) -> list[EvaluationPublic]:
        result = await self.get_many_records(
            session=session, cleaner_id=cleaner.user_id
        )

        return [EvaluationPublic(**res.as_dict()) for res in result]

    @staticmethod
    async def get_cleaner_aggregates(
        session: AsyncSession,
        cleaner: CleanerInfo,
    ) -> EvaluationAggregate:
        """
        Gets general statistics about the cleaning specialist.
        Args:
            session: The database session.
            cleaner: Input data for the identification of the cleaner.

        Returns:
            EvaluationAggregate (pydantic model object): EvaluationAggregate object
            containing statistics about the cleaning specialist.
        """
        stmt = (
            select(
                CleanerEvaluation.cleaner_id,
                func.avg(CleanerEvaluation.professionalism).label(
                    "avg_professionalism"
                ),
                func.avg(CleanerEvaluation.completeness).label("avg_completeness"),
                func.avg(CleanerEvaluation.efficiency).label("avg_efficiency"),
                func.avg(CleanerEvaluation.overall_rating).label("avg_overall_rating"),
                func.min(CleanerEvaluation.overall_rating).label("min_overall_rating"),
                func.max(CleanerEvaluation.overall_rating).label("max_overall_rating"),
                func.count(CleanerEvaluation.owner).label("total_evaluations"),
                func.sum(cast(CleanerEvaluation.no_show, Integer)).label(
                    "total_no_show"
                ),
                func.count(CleanerEvaluation.overall_rating)
                .filter(CleanerEvaluation.overall_rating == 1)
                .label("one_stars"),
                func.count(CleanerEvaluation.overall_rating)
                .filter(CleanerEvaluation.overall_rating == 2)
                .label("two_stars"),
                func.count(CleanerEvaluation.overall_rating)
                .filter(CleanerEvaluation.overall_rating == 3)
                .label("three_stars"),
                func.count(CleanerEvaluation.overall_rating)
                .filter(CleanerEvaluation.overall_rating == 4)
                .label("four_stars"),
                func.count(CleanerEvaluation.overall_rating)
                .filter(CleanerEvaluation.overall_rating == 5)
                .label("five_stars"),
            )
            .where(CleanerEvaluation.cleaner_id == cleaner.user_id)
            .group_by(CleanerEvaluation.cleaner_id)
        )

        res = await session.execute(stmt)
        cleaner_aggregates = res.mappings().one()
        evaluation_aggregate = EvaluationAggregate(
            cleaner=cleaner,
            **cleaner_aggregates,
        )

        return evaluation_aggregate


evaluations_crud = EvaluationsCRUD(CleanerEvaluation)
