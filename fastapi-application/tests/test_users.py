# import pytest
# from fastapi import FastAPI
# from httpx import AsyncClient
#
# pytestmark = pytest.mark.asyncio
#
#
# async def test_user(app: FastAPI, client: AsyncClient) -> None:
#     response = await client.get(app.url_path_for("users:greeting"))
#     message = response.json()
#     assert response.status_code == 200
#     assert message.get("message") == "Hello user!"
