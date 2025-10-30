# app/api/session_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.session_model import Session
from app.core.database import sessions_collection
from app.controllers.auth_controllers import verify_token

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    dependencies=[Depends(verify_token)]
)

@router.post("/")
def create_session(session: Session):
    sessions_collection.insert_one(session.dict())
    return {"message": "Session created successfully", "session": session}

@router.get("/")
def get_sessions():
    return list(sessions_collection.find({}, {"_id": 0}))

@router.get("/{session_id}")
def get_session(session_id: str):
    session = sessions_collection.find_one({"_id": session_id}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}")
def update_session(session_id: str, session: Session):
    result = sessions_collection.update_one({"_id": session_id}, {"$set": session.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session updated successfully"}

@router.delete("/{session_id}")
def delete_session(session_id: str):
    result = sessions_collection.delete_one({"_id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}
