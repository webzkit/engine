from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict

from config import settings

from routes.api import api_router
from core.setup import create_application


# Init application
app = create_application(router=api_router, settings=settings)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=[str(origin)
        #               for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.include_router(api_router, prefix=settings.USER_APP_API_PREFIX)


@app.get("/")
def root() -> Any:
    result: Dict[Any, Any] = {
        "message": f"Your {settings.USER_APP_NAME} endpoint is working"
    }

    return result
