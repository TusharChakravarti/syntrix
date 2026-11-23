from pydantic import BaseModel,ConfigDict

class OrganizationCreate(BaseModel):
    name:str
    slug:str

class OrganizationResponse(BaseModel):
    id:int
    name:str
    slug:str

    model_config = ConfigDict(from_attributes=True)

class OrganizationUpdate(BaseModel):
    name:str | None = None
    slug:str | None = None