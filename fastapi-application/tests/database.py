from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncConnection,
)

# from alembic import (
#     config,
#     command,
# )

from core.models import Base


class DatabaseSessionManager:
    # _ALEMBIC_CFG = config.Config("alembic.ini")

    def __init__(
        self,
    ) -> None:
        self._async_engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    def init(self, url: str) -> None:
        self._async_engine = create_async_engine(
            url=url,
            echo=False,
        )
        self._session_maker = async_sessionmaker(
            bind=self._async_engine,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close(self) -> None:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._async_engine.dispose()
        self._async_engine = None
        self._session_maker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._async_engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        async with self._async_engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # @staticmethod
    # def alembic_upgrade(connection, cfg) -> None:
    #     cfg.attributes["connection"] = connection
    #     command.upgrade(config=cfg, revision="head")

    # @staticmethod
    # def alembic_downgrade(connection, cfg) -> None:
    #     cfg.attributes["connection"] = connection
    #     command.downgrade(config=cfg, revision="base")

    @staticmethod
    async def create_all(connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_all(connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.drop_all)


session_manager = DatabaseSessionManager()
