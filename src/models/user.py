import uuid as uuid_pkg

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from db.models import UUIDMixin
from db.models import SoftDeleteMixin, TimestampMixin


class User(UUIDMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    # uuid: Mapped[uuid_pkg.UUID] = mapped_column(
    #    default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    # )

    group_id: Mapped[int | None] = mapped_column(
        ForeignKey("groups.id"), index=True, default=None, init=False
    )
