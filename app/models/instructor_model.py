from pydantic import BaseModel, Field, validator
from typing import Optional

class Instructor(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB _id
    name: str = Field(..., min_length=2, max_length=100)
    role: Optional[str] = Field(None, max_length=50)
    model_version: Optional[str] = Field(None, max_length=20)
    expertise: str = Field(..., min_length=2, max_length=100)

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
