from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String
from db.database import Base
from db.models import UUIDMixin, TimestampMixin, SoftDeleteMixin
from datetime import UTC, datetime


class Group(SoftDeleteMixin, Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(30))

    #created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    #updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    #deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    #is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

