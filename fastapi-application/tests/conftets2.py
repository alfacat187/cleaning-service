# from typing import AsyncGenerator
# import asyncio
#
# import pytest
# import pytest_asyncio
# from httpx import (
#     AsyncClient,
#     ASGITransport,
# )
# from asgi_lifespan import LifespanManager
# from pytest_postgresql import factories
# from pytest_postgresql.janitor import DatabaseJanitor
#
# from server.create_fastapi_app import create_app
# from tests.database import session_manager
# from core.models import db_helper
#
#
# @pytest.fixture(autouse=True)
# def app():
#     _app = create_app()
#
#     return _app
#
#
# @pytest_asyncio.fixture(scope="module")
# async def client(app) -> AsyncGenerator[AsyncClient, None]:
#     async with LifespanManager(app):
#         transport = ASGITransport(app=app)
#         async with AsyncClient(
#             transport=transport,
#             base_url="http://test",
#             headers={"Content-Type": "application/json"},
#         ) as client:
#
#             yield client
#
#
# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()
#
#
# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def connection_test(event_loop):
#     test_db = factories.postgresql_proc(host="localhost", port=5432, dbname="test_db")
#     pg_host = test_db.host
#     pg_port = test_db.port
#     pg_user = test_db.user
#     pg_db = test_db.dbname
#     pg_password = test_db.password
#
#     with DatabaseJanitor(
#         pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
#     ):
#         connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
#         session_manager.init(connection_str)
#         yield
#         await session_manager.close()
#
#
# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def create_tables(connection_test):
#     async with session_manager.connect() as connection:
#         await session_manager.drop_all(connection)
#         await session_manager.create_all(connection)
#
#
# @pytest.fixture(scope="function", autouse=True)
# async def session_override(app, connection_test):
#     async def get_db_override():
#         async with session_manager.session() as session:
#             yield session
#
#     app.dependency_overrides[db_helper.session_getter] = get_db_override
