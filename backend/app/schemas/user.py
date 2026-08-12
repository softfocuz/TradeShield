from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import UserRole
from app.schemas.profile import ExporterProfileRead, ImporterProfileRead


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    is_active: bool = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    exporter_profile: Optional[ExporterProfileRead] = None
    importer_profile: Optional[ImporterProfileRead] = None
