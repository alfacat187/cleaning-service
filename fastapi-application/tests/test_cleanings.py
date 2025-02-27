# import pytest
# from fastapi import (
#     FastAPI,
#     status,
# )
# from httpx import AsyncClient
#
# from api.api_v1.cleanings.schemas import (
#     CleaningCreate,
#     CleaningPublic,
# )
#
# pytestmark = pytest.mark.asyncio
#
#
# @pytest.fixture
# def create_cleaning():
#     return CleaningCreate(
#         name="test cleaning",
#         price=20.0,
#         description="cleaning for test",
#         cleaning_type="spot clean",
#     )
#
#
# class TestCleaningsRoutes:
#
#     async def test_cleanings_routes(
#         self,
#         app: FastAPI,
#         client: AsyncClient,
#     ) -> None:
#         response = await client.post(
#             app.url_path_for("cleanings:create-cleaning"),
#             json={},
#         )
#         assert response.status_code != status.HTTP_404_NOT_FOUND
#
#     async def test_invalid_input_raises_error(
#         self,
#         app: FastAPI,
#         client: AsyncClient,
#     ) -> None:
#         response = await client.post(
#             app.url_path_for("cleanings:create-cleaning"),
#             json={},
#         )
#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
#
#
# class TestCleaning:
#     async def test_valid_input_creates_new_cleaning(
#         self,
#         app: FastAPI,
#         client: AsyncClient,
#         create_cleaning: CleaningCreate,
#     ) -> None:
#         response = await client.post(
#             app.url_path_for("cleanings:create-cleaning"),
#             json={**create_cleaning.model_dump()},
#         )
#         created_cleaning = CleaningPublic(**response.json())
#         assert response.status_code == status.HTTP_201_CREATED
#         assert created_cleaning.name == "test cleaning"
#         assert created_cleaning.price == 20.0
#         assert created_cleaning.description == "cleaning for test"
#         assert created_cleaning.cleaning_type == "spot clean"
#
#     @pytest.mark.parametrize(
#         "payload, status_code",
#         [
#             (
#                 {
#                     "name": None,
#                     "price": None,
#                     "description": "test description",
#                     "cleaning_type": "spot clean",
#                 },
#                 422,
#             ),
#             (
#                 {
#                     "name": "alex",
#                     "price": None,
#                     "description": "test description",
#                     "cleaning_type": "spot clean",
#                 },
#                 422,
#             ),
#             (
#                 {
#                     "name": "alex",
#                     "price": 12.0,
#                     "description": None,
#                     "cleaning_type": "dast upp",
#                 },
#                 422,
#             ),
#             (
#                 {
#                     "name": 12.0,
#                     "price": "some price",
#                     "description": None,
#                     "cleaning_type": "dust up",
#                 },
#                 422,
#             ),
#         ],
#     )
#     async def test_create_cleaning_invalid_input(
#         self,
#         app: FastAPI,
#         client: AsyncClient,
#         payload,
#         status_code,
#     ) -> None:
#         response = await client.post(
#             app.url_path_for("cleanings:create-cleaning"),
#             json=payload,
#         )
#         assert response.status_code == status_code
#
#
# class TestGetCleaning:
#     async def test_get_cleaning_by_id(
#         self,
#         app: FastAPI,
#         client,
#         create_cleaning_to_db,
#     ) -> None:
#         response = await client.get(
#             app.url_path_for(
#                 "cleanings:get-cleaning-by-id", cleaning_id=create_cleaning_to_db.id
#             )
#         )
#         db = create_cleaning_to_db
#         print(create_cleaning_to_db.name)
#         print(response.json())
#         assert response.status_code == 200
