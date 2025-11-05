from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.session_model import Session, SessionResponse
from app.controllers.session_controllers import SessionController
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from app.core.permissions import require_admin, require_own_or_admin,require_session_owner_or_admin,require_user_or_instructor

db = Database()
session_controller = SessionController(db)
auth_controller = AuthController(db)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    dependencies=[Depends(auth_controller.verify_token)]
)

@router.post("/", response_model=SessionResponse,dependencies=[Depends(require_admin)])
def create_session(session: Session):
    created = session_controller.create_session(session)
    return created

@router.get("/", response_model=List[SessionResponse],dependencies=[Depends(require_admin)])
def get_sessions():
    return session_controller.get_sessions()

@router.get("/{session_id}", response_model=SessionResponse,dependencies=[Depends(require_session_owner_or_admin)])
def get_session(session_id: str):
    session = session_controller.get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}",dependencies=[Depends(require_session_owner_or_admin)])
def update_session(session_id: str, session: Session):
    updated_count = session_controller.update_session_by_id(session_id, session)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session updated successfully"}

@router.delete("/{session_id}",dependencies=[Depends(require_admin)])
def delete_session(session_id: str):
    deleted_count = session_controller.delete_session_by_id(session_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}
