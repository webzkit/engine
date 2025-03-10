from time import sleep
from config import settings
import consul

"""
def register_to_consul():
    consul_host = configuration.CONSUL_HOST
    consul_port = configuration.CONSUL_PORT
    url = f"http://{consul_host}:{consul_port}/v1/agent/service/register"
    data = {
        "Name": "school",
        "Tags": ["school"],
        "Address": configuration.address,
        "Port": configuration.port,
        "Check": {
            "http": f"http://{configuration.address}:{configuration.port}/health",
            "interval": "10s",
        },
        "connect": {
            "sidecar_service": {
                "proxy": {
                    "upstreams": [
                        {"destination_name": "student", "local_bind_port": 3000}
                    ]
                }
            }
        },
    }
    res = {"message": "registering"}
    res = httpx.put(url, data=json.dumps(data))
    return res.text
"""


async def register():
    check_http = consul.Check.http(
        f"http://{settings.CONTAINER_NAME}:8000/health", interval="10s"
    )
    client = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)

    while True:
        try:
            client.agent.service.register(
                name=settings.ENGINE_APP_NAME,
                address=settings.CONTAINER_NAME,
                port=8000,
                check=check_http,
            )
            break
        except consul.ConsulException:
            print("Retrying to connect to consul ...")
            sleep(0.5)
