from pydantic import BaseModel


class ExporterBase(BaseModel):
    company_name: str
    business_registration: str
    country: str


class ExporterCreate(ExporterBase):
    pass


class ImporterBase(BaseModel):
    company_name: str
    import_license: str
    destination_country: str


class ImporterCreate(ImporterBase):
    pass
