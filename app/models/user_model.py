# app/models/user_model.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # MongoDB _id as string
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    level: str = Field(..., min_length=1, max_length=20)
    password: str = Field(..., min_length=6)

    @validator("password", pre=True)
    def truncate_password(cls, v):
        """
        Enforce MongoDB-compatible password byte size (max 72 bytes for bcrypt)
        """
        if isinstance(v, str):
            return v.encode("utf-8")[:72].decode("utf-8", "ignore")
        return v

    class Config:
        allow_population_by_field_name = True
        orm_mode = True  # allows compatibility with ORMs or dicts
