from app.core.database import Database
from app.models.user_model import UserCreate
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class AuthController:
    def __init__(self, db: Database):
        self.users_collection = db.users
        # JWT settings
        self.SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 1))
        # Password hashing
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # Security scheme
        self.security = HTTPBearer()

    # --- Helper functions ---
    def hash_password(self,password: str) -> str:
        password_bytes = password.encode("utf-8")[:72]
        password_truncated = password_bytes.decode("utf-8", "ignore")
        return self.pwd_context.hash(password_truncated)

    def verify_password(self,plain_password: str, hashed_password: str) -> bool:
        password_bytes = plain_password.encode("utf-8")[:72]
        plain_truncated = password_bytes.decode("utf-8", "ignore")
        return self.pwd_context.verify(plain_truncated, hashed_password)

    def create_access_token(self,data: Dict[str, str]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=self.ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing token"
            )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: str = payload.get("sub")
            role: str = payload.get("role")
            if user_id is None or role is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token payload"
                )
            return {"id": user_id, "role": role}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is invalid or expired"
            )

    # --- Auth logic functions ---

    def signup_logic(self, user: UserCreate):
        if self.users_collection.find_one({"username": user.username}):
            return None, "Username already exists"
        user_dict = user.dict()
        user_dict["password"] = self.hash_password(user.password)
        result = self.users_collection.insert_one(user_dict)
        return str(result.inserted_id), None

    def login_logic(self, username: str, password: str):
        user = self.users_collection.find_one({"username": username})
        if not user or not self.verify_password(password, user["password"]):
            return None, "Invalid username or password"
        role = user.get("role", "user")  # default role fallback
        token = self.create_access_token({"sub": str(user["_id"]), "role": role})
        return token, None

