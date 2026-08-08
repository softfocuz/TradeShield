from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class ExporterProfile(Base):
    __tablename__ = "exporter_profiles"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    business_registration: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="exporter_profile")


class ImporterProfile(Base):
    __tablename__ = "importer_profiles"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    import_license: Mapped[str] = mapped_column(String(255), nullable=False)
    destination_country: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="importer_profile")
