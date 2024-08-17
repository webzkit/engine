from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict, Optional
import os

from config import settings

from routes.v1.api import api_router


app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.APP_API_PREFIX}/openapi.json"
)

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

app.include_router(api_router, prefix=settings.APP_API_PREFIX)


@app.get("/")
def root(
    cpu_load: Optional[str] = Query(
        False,
        description='True/False depending your needs, gets average CPU load value',
        regex='^(True|False)$')
) -> Any:
    result: Dict[Any, Any] = {
        "message": "Your first endpoint is working"
    }

    if cpu_load == 'True':
        result["cpu_average_load"] = os.getloadavg()
        result["cpu"] = os.cpu_count()
    return result
