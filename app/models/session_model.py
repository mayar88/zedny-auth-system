from pydantic import BaseModel, Field, validator,field_validator
from app.models.instructor_model import InstructorResponse
from app.models.user_model import UserResponse
from typing import Optional
from datetime import datetime,timezone,timedelta



class Session(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100)
    session_date: datetime
    instructor_id: str = Field(..., description="MongoDB _id of the instructor")
    user_id: str = Field(..., description="MongoDB _id of the user")

    @field_validator("session_date")
    @classmethod
    def validate_date_not_in_past(cls, v: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        max_future_date = now + timedelta(days=5*365)
        if v < now:
            raise ValueError("Session date cannot be in the past.")
        if v > max_future_date:
            raise ValueError("Session date cannot be more than 5 years in the future.")
        return v


class SessionResponse(BaseModel):
    id: str = Field(..., alias="_id")
    topic: str
    session_date: datetime
    instructor: Optional[InstructorResponse] = None
    user: Optional[UserResponse] = None

    class Config:
        allow_population_by_field_name = True