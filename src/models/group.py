from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from db.database import Base
from db.models import TimestampMixin, SoftDeleteMixin


class Group(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(30), nullable=False)

