from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict

from config import settings

from apis.api import api_router
from core.setup import create_application


# from core.event.consumer import ConsumerEvent
# import asyncio


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


# USER_SERVICE_TOPIC = "user_service"
# loop = asyncio.get_event_loop()
# kafka_consumer = None


"""
def consume_kafka():
    global kafka_consumer
    kafka_consumer = ConsumerEvent(USER_SERVICE_TOPIC, loop)
    asyncio.create_task(kafka_consumer.consume())


consume_kafka()
"""


@app.get("/")
def root() -> Any:
    result: Dict[Any, Any] = {
        "message": f"Your {settings.ENGINE_APP_NAME} endpoint is working"
    }

    return result


@app.get("/health")
def health_status():
    return {"status": "healthy"}
