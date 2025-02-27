from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    and_,
    delete,
    update,
)

from crud.base import CRUDRepository
from api.api_v1.offers.models import UserOffer
from api.api_v1.offers.schemas import (
    OfferInDB,
    OfferPublic,
    UserInfo,
    OfferUpdate,
)
from api.api_v1.profiles.models import Profile


class OfferCrud(CRUDRepository):  # type: ignore

    @staticmethod
    async def get_user_offer(
        session: AsyncSession,
        user_id: UUID,
        cleaning_id: int,
    ) -> UserOffer | None:
        """
        Retrieves the user's offer from the database.
        Args:
            session: The database session.
            user_id: User identifier.
            cleaning_id: Cleaning identifier.

        Returns:
                UserOffer object if found, otherwise None.
        """
        offer = await session.execute(
            select(UserOffer).where(
                and_(
                    UserOffer.offerer_id == user_id,
                    UserOffer.cleaning_id == cleaning_id,
                )
            )
        )

        return offer.scalar()

    async def create_new_offer(
        self,
        session: AsyncSession,
        offer_schema: OfferInDB,
    ) -> OfferPublic | None:
        """
        Creates the user's offer.
        Args:
            session: The database session.
            offer_schema: Input data for creating an offer.

        Returns:
            OfferPublic (pydantic model object) | None: User offer object if it
            does not exist in the database, otherwise None.
        """
        offer_exists = await self.get_user_offer(
            session=session,
            user_id=offer_schema.offerer_id,
            cleaning_id=offer_schema.cleaning_id,
        )
        if offer_exists:
            return None

        offer = await self.create_record(
            session=session,
            obj_in=OfferInDB(**offer_schema.model_dump()),
        )

        return OfferPublic(**offer.as_dict())

    @staticmethod
    async def get_user_info_from_profile(
        session: AsyncSession,
        user_id: UUID,
    ) -> UserInfo:
        """
        Retrieves the user's profile from the database.

        Users without a profile cannot create cleanings or offers.
        This method is called after checking if there is an offer or
        cleaning in the database. Therefore, the profile is in the database.
        Args:
            session: The database session.
            user_id: User identifier.

        Returns:
            UserInfo (pydantic model object): UserInfo object containing
            information from the profile.
        """
        res = await session.scalar(select(Profile).filter_by(user_id=user_id))

        return UserInfo(**res.as_dict())

    async def get_all_offers_for_offerer(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> list[UserOffer]:
        """
        Gets all offers by offerer identifier.
        Args:
            session: The database session.
            user_id: User identifier.

        Returns:
                List of UserOffer objects.
        """
        res = await self.get_many_records(
            session=session,
            offerer_id=user_id,
        )

        return res

    @staticmethod
    async def get_offers_with_status(
        session: AsyncSession,
        user_id: UUID,
        status: str,
    ) -> list[OfferPublic]:
        """
        Gets all offers by offerer ID and status.
        Args:
            session: The database session.
            user_id: User identifier.
            status: Offer status.

        Returns:
            list[OfferPublic] (pydantic model object): List of user offer objects.
        """
        result = await session.scalars(
            select(UserOffer).where(
                and_(UserOffer.offerer_id == user_id, UserOffer.status == status)
            )
        )
        return [OfferPublic(**res.as_dict()) for res in result.all()]

    @staticmethod
    async def delete_offers_with_status(
        session: AsyncSession,
        user_id: UUID,
        status: str,
    ) -> None:
        """
        Deletes all offers for an offerer with a specific status.
        Args:
            session: The database session.
            user_id: User identifier.
            status: Offer status.
        """
        await session.execute(
            delete(UserOffer).where(
                and_(UserOffer.offerer_id == user_id, UserOffer.status == status)
            )
        )
        await session.commit()

    async def get_offers_for_cleaning_owner(
        self,
        session: AsyncSession,
        cleaning_id: int,
        offset: int,
        limit: int,
    ) -> list[UserOffer]:
        """
        Gets all offers for cleaner by cleaning ID.
        Args:
            session: The database session.
            cleaning_id: Cleaning identifier.
            offset: The number of results to skip.
            limit: The maximum number of results to return.

        Returns:
                List of UserOffer objects.
        """
        offers = await self.get_many_records(
            session=session,
            cleaning_id=cleaning_id,
            offset=offset,
            limit=limit,
        )

        return offers

    @staticmethod
    async def update_offer_for_cleaning_owner(
        session: AsyncSession,
        offer: OfferPublic,
        offer_update: OfferUpdate,
    ) -> UserOffer:
        """
        Updates offer by offerer ID and cleaning ID.
        Args:
            session: The database session.
            offer: Input data to identify the offer.
            offer_update: Input data to update the offer.

        Returns:
                UserOffer object.
        """
        to_update = await session.scalar(
            update(UserOffer)
            .where(
                and_(
                    UserOffer.offerer_id == offer.offerer_id,
                    UserOffer.cleaning_id == offer.cleaning_id,
                )
            )
            .values(status=offer_update.status)
            .returning(UserOffer)
        )
        await session.flush()
        await session.commit()

        return to_update


offers_crud = OfferCrud(UserOffer)
