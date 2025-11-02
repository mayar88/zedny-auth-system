from pydantic import BaseModel, Field
from typing import Optional
from app.models.instructor_model import InstructorResponse
from app.models.user_model import UserResponse


class Session(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100)
    date: str = Field(..., description="Session date, e.g., '2025-10-30'")
    instructor_id: str = Field(..., description="MongoDB _id of the instructor")
    user_id: str = Field(..., description="MongoDB _id of the user")

class SessionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    topic: str
    date: str
    instructor: InstructorResponse
    user: UserResponse

    class Config:
        allow_population_by_field_name = True
