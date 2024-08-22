from typing import Any

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Response:
    def __init__(self):
        pass

    @staticmethod
    def results(data: Any, status_code: int = 200):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": True,
                "items": jsonable_encoder(data)
            }
        )

    @staticmethod
    def result(data: Any, status_code: int = 200):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": True,
                "item": jsonable_encoder(data)
            }
        )

    @staticmethod
    def message(message: str, status_code: int = 200, status: bool = True):
        return JSONResponse(
            status_code=status_code,
            content={
                "status": status,
                "message": message
            }
        )
