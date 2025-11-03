from fastapi import APIRouter, HTTPException
from app.controllers.auth_controllers import AuthController
from app.models.user_model import UserCreate
from app.core.database import Database

db = Database()
auth_controller = AuthController(db)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup_logic(user: UserCreate):
    user_id, error = auth_controller.signup_logic(user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User created successfully", "user_id": user_id}

@router.post("/login")
def login_logic(username: str, password: str):
    token, error = auth_controller.login_logic(username, password)
    if error:
        raise HTTPException(status_code=401, detail=error)
    return {"access_token": token, "token_type": "bearer"}
