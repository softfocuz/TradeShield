from typing import Optional, Union
from pydantic import BaseModel, EmailStr, model_validator
from app.models.user import UserRole
from app.schemas.profile import ExporterCreate, ImporterCreate


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    exporter_profile: Optional[ExporterCreate] = None
    importer_profile: Optional[ImporterCreate] = None

    @model_validator(mode="after")
    def validate_profile_for_role(self) -> "UserRegister":
        if self.role == UserRole.EXPORTER:
            if not self.exporter_profile:
                raise ValueError("exporter_profile is required when role is EXPORTER")
            if self.importer_profile:
                raise ValueError("importer_profile should not be provided when role is EXPORTER")
        elif self.role == UserRole.IMPORTER:
            if not self.importer_profile:
                raise ValueError("importer_profile is required when role is IMPORTER")
            if self.exporter_profile:
                raise ValueError("exporter_profile should not be provided when role is IMPORTER")
        return self
