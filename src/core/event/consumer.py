from aiokafka import AIOKafkaConsumer
import logging


KAFKA_BOOTSTRAP_SERVERS = "kafka:29092"


kafka_bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ConsumerEvent:
    def __init__(self, topic: str, loop):
        self.consumer = AIOKafkaConsumer(
            topic, loop=loop, bootstrap_servers=kafka_bootstrap_servers
        )

    async def consume(self):
        try:
            await self.consumer.start()
        except Exception as e:
            logging.info(str(e))
            return

        try:
            async for msg in self.consumer:
                test = msg.value.decode("utf-8")  # pyright: ignore
                print(test)
        finally:
            await self.consumer.stop()
