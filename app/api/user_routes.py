from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.user_model import UserCreate, UserResponse
from app.controllers.user_controllers import UserController
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from app.core.permissions import require_admin, require_own_or_admin
db = Database()
user_controller = UserController(db)
auth_controller = AuthController(db)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(auth_controller.verify_token)]
)

@router.post("/", response_model=UserResponse , dependencies=[Depends(require_admin)])
def create_user(user: UserCreate):
    created_user, error = user_controller.create_user(user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return created_user

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_admin)])
def get_users():
    return user_controller.get_all_users()

@router.get("/{user_id}", response_model=UserResponse , dependencies=[Depends(require_own_or_admin)])
def get_user(user_id: str):
    user = user_controller.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}",dependencies=[Depends(require_own_or_admin)])
def update_user(user_id: str, user: UserCreate):
    matched_count = user_controller.update_user_by_id(user_id, user)
    if matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}

@router.delete("/{user_id}" ,  dependencies=[Depends(require_admin)])
def delete_user(user_id: str):
    deleted_count = user_controller.delete_user_by_id(user_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
