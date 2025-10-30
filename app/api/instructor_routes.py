# app/api/instructor_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.instructor_model import Instructor
from app.core.database import instructors_collection
from app.controllers.auth_controllers import verify_token

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
    dependencies=[Depends(verify_token)]
)

@router.post("/")
def create_instructor(instructor: Instructor):
    if instructors_collection.find_one({"name": instructor.name}):
        raise HTTPException(status_code=400, detail="Instructor already exists")
    instructors_collection.insert_one(instructor.dict())
    return {"message": "Instructor created successfully", "instructor": instructor}

@router.get("/")
def get_instructors():
    return list(instructors_collection.find({}, {"_id": 0}))

@router.get("/{instructor_id}")
def get_instructor(instructor_id: str):
    instructor = instructors_collection.find_one({"_id": instructor_id}, {"_id": 0})
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.put("/{instructor_id}")
def update_instructor(instructor_id: str, instructor: Instructor):
    result = instructors_collection.update_one({"_id": instructor_id}, {"$set": instructor.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor updated successfully"}

@router.delete("/{instructor_id}")
def delete_instructor(instructor_id: str):
    result = instructors_collection.delete_one({"_id": instructor_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor deleted successfully"}
