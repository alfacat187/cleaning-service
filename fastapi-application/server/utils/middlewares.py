from contextvars import ContextVar

from fastapi import (
    Request,
    Response,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

request_object: ContextVar[Request] = ContextVar("request")


class PaginationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_object.set(request)
        response = await call_next(request)

        return response
