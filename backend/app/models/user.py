import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.profile import ExporterProfile, ImporterProfile


class UserRole(str, enum.Enum):
    EXPORTER = "EXPORTER"
    IMPORTER = "IMPORTER"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    exporter_profile: Mapped[Optional["ExporterProfile"]] = relationship(
        "ExporterProfile", back_populates="user", uselist=False
    )
    importer_profile: Mapped[Optional["ImporterProfile"]] = relationship(
        "ImporterProfile", back_populates="user", uselist=False
    )
