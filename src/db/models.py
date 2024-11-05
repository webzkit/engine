import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class UUIDMixin(MappedAsDataclass):
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid_pkg.uuid4(), unique=True, kw_only=True,
    )


class TimestampMixin(MappedAsDataclass):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), kw_only=True
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, kw_only=True
    )


class SoftDeleteMixin(MappedAsDataclass):
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None, kw_only=True
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, kw_only=True)
