from time import sleep
from config import settings
import consul


async def register():
    check_http = consul.Check.http(
        f"http://{settings.SERVICE_NAME}:8000/health", interval="10s", timeout="5s"
    )
    client = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)

    while True:
        try:
            client.agent.service.register(
                name=settings.SERVICE_NAME,
                address=settings.SERVICE_NAME,
                port=8000,
                check=check_http,
                tags=["api", "engine"],
            )
            break
        except consul.ConsulException:
            print("Retrying to connect to consul ...")
            sleep(0.5)
