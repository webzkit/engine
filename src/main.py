from typing import Any, Dict
from config import settings
from apis.api import api_router
from core.setup import create_application


# Init application
app = create_application(router=api_router, settings=settings)


@app.get("/")
def root() -> Any:
    result: Dict[Any, Any] = {
        "message": f"Your {settings.APP_NAME} endpoint is working"
    }

    return result


@app.get("/health")
def health_status():

    return {"status": "healthy"}
