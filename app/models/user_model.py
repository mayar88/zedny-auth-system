from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    level: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=6)

    @validator("password", pre=True)
    def truncate_password(cls, v):
        if isinstance(v, str):
            return v.encode("utf-8")[:72].decode("utf-8", "ignore")
        return v

class UserResponse(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    email: str
    level: str

    class Config:
        allow_population_by_field_name = True