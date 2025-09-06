from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from core.logging.logger import Logger
from core.helpers.utils import sanitize_path, parse_query_str
from starlette.types import ASGIApp


logger = Logger("http-request", filename="http-request.log")
SKIP_LOGGER = ["health", "metrics"]


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def get_uname(self, request: Request) -> Response | Any:
        request_init_data = request.headers.get("request-init-data")

        if request_init_data is None:
            return "Guest"

        get_current_user = parse_query_str(request_init_data)

        return get_current_user.get("name", "Guest")

    async def get_body(self, request: Request) -> str:
        body = await request.body()

        return body.decode("utf-8", errors="replace")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        path = sanitize_path(request.url.path)
        if path in SKIP_LOGGER:
            return await call_next(request)

        uname = await self.get_uname(request)
        client_host = request.client.host  # pyright: ignore
        request_body = await self.get_body(request)

        # loggerwarning(f"Test Warning")
        # logger.critical(f"Test Critical")
        # logger.info(f"Test Info")
        # logger.error(f"Test Error")
        # logger.debug(f"Test Debug")

        response: Response = await call_next(request)

        # Log acccess
        logger.info(
            f"Request: {request.method} {request.url}",
            extra={
                "uname": uname,
                "client_host": client_host,
                "request_body": request_body,
                "status_code": response.status_code,
                "method": request.method,
                "path": request.url.path,
            },
        )

        return response
