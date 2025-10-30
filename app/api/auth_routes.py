# app/api/auth_routes.py
from fastapi import APIRouter, HTTPException
from app.controllers.auth_controllers import signup_logic, login_logic
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user: User):
    user_id, error = signup_logic(user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User created successfully", "user_id": user_id}

@router.post("/login")
def login(username: str, password: str):
    token, error = login_logic(username, password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"access_token": token, "token_type": "bearer"}
