from app.models.user_model import User
from app.core.database import users_collection   # <- correct
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Dict
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Load environment variables
load_dotenv()

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 1))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# old version  if i need use username and password i will use this way 'auth2passwordbearer'
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

security = HTTPBearer()



# --- Helper functions ---

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    password_truncated = password_bytes.decode("utf-8", "ignore")
    return pwd_context.hash(password_truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    plain_truncated = password_bytes.decode("utf-8", "ignore")
    return pwd_context.verify(plain_truncated, hashed_password)

def create_access_token(data: Dict[str, str]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token"
        )
    # (Optional) You can decode/verify your JWT token here if needed.
    return token

# --- Auth logic functions ---

def signup_logic(user: User):
    if users_collection.find_one({"username": user.username}):
        return None, "Username already exists"
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    result = users_collection.insert_one(user_dict)
    return str(result.inserted_id), None

def login_logic(username: str, password: str):
    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None, "Invalid username or password"
    token = create_access_token({"sub": str(user["_id"])})
    return token, None
