from pydantic import BaseModel, Field
from typing import Optional


class InstructorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=50)
    model_version: Optional[str] = Field(None, max_length=20)
    expertise: str = Field(..., min_length=2, max_length=100)


class InstructorResponse(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    role: str
    expertise: str

    class Config:
        allow_population_by_field_name = True
