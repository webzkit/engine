import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import  DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid_pkg.uuid4,
        unique=True
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC)
    )

    updated_at: Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True), default=None
    )


class SoftDeleteMixin:
    deleted_at: Mapped[datetime|None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted:Mapped[bool] = mapped_column(default=False)



