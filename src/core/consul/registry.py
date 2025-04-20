from config import settings
import consul
import asyncio


async def register_service():
    check_http = consul.Check.http(
        f"http://{settings.SERVICE_NAME}:{settings.SERVICE_PORT}/health",
        interval=f"{settings.CONSUL_INTERVAL}",
        timeout=f"{settings.CONSUL_TIMEOUT}",
    )
    client = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)

    while True:
        try:
            client.agent.service.register(
                name=settings.SERVICE_NAME,
                address=settings.SERVICE_NAME,
                port=settings.SERVICE_PORT,
                check=check_http,
                tags=["api", "engine"],
            )
            break
        except consul.ConsulException:
            print("Retrying to connect to consul ...")
            await asyncio.sleep(0.5)
