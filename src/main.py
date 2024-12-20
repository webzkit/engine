from starlette.middleware.cors import CORSMiddleware
from typing import Any, Dict, List

from config import settings

from apis.api import api_router
from core.setup import create_application

# kafka
from random import shuffle
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import json


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

SPIDEY_NAMES = "Tom Holland,Andrew Garfield,Tobey Maguire"
KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"
SPIDERWEB_TOPIC = "spiderweb"
my_name: str = "User"

spidey_names: List[Any] = SPIDEY_NAMES.split(",")
kafka_bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS
spiderweb_topic: str = SPIDERWEB_TOPIC

loop = asyncio.get_event_loop()


mapping_place = {
    3: "name is the Winner!!!",
    2: "name is the Second Place!!!",
    1: "name is the third Place!!!",
}


async def send_one(topic: str, msg: List):
    try:
        producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
        await producer.start()

        try:
            await producer.send_and_wait(topic, kafka_serializer(msg))
        finally:
            await producer.stop()

    except Exception as err:
        print(f"Some Kafka error: {err}")


def spidey_random(spidey_list: List) -> List:
    shuffle(spidey_list)
    return spidey_list


async def play_turn(finalists: List):
    spidey_order = spidey_random(finalists)
    await send_one(topic=spiderweb_topic, msg=spidey_order)


def kafka_serializer(value):
    return json.dumps(value).encode()


def encode_json(msg):
    to_load = msg.value.decode("utf-8")
    return json.loads(to_load)


def check_spidey(finalists: List) -> bool:
    return my_name == finalists[0]


async def spiderweb_turn(msg):
    finalists = encode_json(msg)
    is_my_turn = check_spidey(finalists)

    if is_my_turn:
        print(mapping_place[len(finalists)].replace("name", my_name))

        if len(finalists) > 1:
            finalists.pop(0)
            await play_turn(finalists)


kafka_actions = {
    "spiderweb": spiderweb_turn,
}


async def consume():
    consumer = AIOKafkaConsumer(
        spiderweb_topic,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
    )

    print(spiderweb_topic)

    try:
        await consumer.start()

    except Exception as e:
        print(e)
        return

    try:
        async for msg in consumer:
            await kafka_actions[msg.topic](msg)

    finally:
        await consumer.stop()


asyncio.create_task(consume())


@app.get("/")
def root() -> Any:
    result: Dict[Any, Any] = {
        "message": f"Your {settings.ENGINE_APP_NAME} endpoint is working"
    }

    return result
