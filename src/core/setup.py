from typing import Any, AsyncGenerator, Callable
from fastapi import APIRouter, FastAPI
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
import fastapi
from fastapi.openapi.utils import get_openapi
from middlewares.metrics import MetricMiddleware, metrics
from middlewares.log_request import LogRequestMiddleware

from config import (
    EnviromentOption,
    RegisterServiceSetting,
    AppSetting,
    RedisCacheSetting,
    PostgresSetting,
)
from core.redis.redis_pool import redis_pool


redis_cache = None


# Cache
async def create_redis_cache_pool() -> None:
    global redis_cache
    redis_cache = redis_pool


async def close_redis_cache_pool() -> None:
    await redis_cache.close()  # type: ignore


def lifespan_factory(
    settings: AppSetting | RedisCacheSetting | PostgresSetting | RegisterServiceSetting,
) -> Callable[[FastAPI], _AsyncGeneratorContextManager[Any]]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:  # piright: ignore
        if isinstance(settings, RedisCacheSetting):
            await create_redis_cache_pool()
        yield

        if isinstance(settings, RedisCacheSetting):
            await close_redis_cache_pool()

    return lifespan


# Create Applications
def create_application(
    router: APIRouter, settings: AppSetting, **kwargs: Any
) -> FastAPI:
    if isinstance(settings, AppSetting):
        to_update = {
            "title": settings.APP_NAME,
            "description": "Description",
            "docs_url": None,
            "redoc_url": None,
            "openapi_url": None,
        }

        kwargs.update(to_update)

    lifespan = lifespan_factory(settings)
    application = FastAPI(lifespan=lifespan, **kwargs)

    # Setting metrics middleware
    if isinstance(settings, AppSetting):
        # Logger
        application.add_middleware(LogRequestMiddleware)

        application.add_middleware(MetricMiddleware, app_name=settings.APP_NAME)
        application.add_route("/metrics", metrics)

    if isinstance(settings, AppSetting):
        application.include_router(router, prefix=settings.APP_API_PREFIX)

    if isinstance(settings, AppSetting):
        if settings.APP_ENV != EnviromentOption.PRODUCTION.value:
            docs_router = APIRouter()

            @docs_router.get("/docs", include_in_schema=False)
            async def get_swagger_documentation() -> fastapi.responses.HTMLResponse:
                return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/redoc", include_in_schema=False)
            async def get_redoc_documentation() -> fastapi.responses.HTMLResponse:
                return get_redoc_html(openapi_url="/openapi.json", title="docs")

            @docs_router.get("/openapi.json", include_in_schema=False)
            async def openapi() -> dict[str, Any]:
                out: dict = get_openapi(
                    title=application.title,
                    version=application.version,
                    routes=application.routes,
                )

                return out

            application.include_router(docs_router)

    return application
