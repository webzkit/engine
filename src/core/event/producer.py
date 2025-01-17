import json
import logging
from typing import Any
from aiokafka import AIOKafkaProducer


KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"


kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ProducerEvent:
    topic: str

    def __init__(self, topic: str):
        self.topic = topic

    async def produce(self, value: Any):
        try:
            producer = AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)
            await producer.start()
            try:
                await producer.send_and_wait(self.topic, self.serializer(value))
            finally:
                await producer.stop()
        except Exception as err:
            logging.error(f"Some Kafka error: {err}")

    def serializer(self, value: Any):
        return json.dumps(value).encode()
