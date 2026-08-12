from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ExporterBase(BaseModel):
    company_name: str
    business_registration: str
    country: str


class ExporterCreate(ExporterBase):
    pass


class ExporterProfileRead(ExporterBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID


class ExporterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    business_registration: Optional[str] = None
    country: Optional[str] = None


class ImporterBase(BaseModel):
    company_name: str
    import_license: str
    destination_country: str


class ImporterCreate(ImporterBase):
    pass


class ImporterProfileRead(ImporterBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID


class ImporterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    import_license: Optional[str] = None
    destination_country: Optional[str] = None
