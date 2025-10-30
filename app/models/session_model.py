from pydantic import BaseModel, Field
from typing import Optional

class Session(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB _id
    topic: str = Field(..., min_length=2, max_length=100)
    date: str = Field(..., description="Session date, e.g., '2025-10-30'")
    instructor_id: str = Field(..., description="MongoDB _id of the instructor")
    user_id: str = Field(..., description="MongoDB _id of the user")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True