from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime
import datetime


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=datetime.datetime.now())

    @declared_attr
    def updated_at(self):
        return Column(DateTime, default=datetime.datetime.now())
