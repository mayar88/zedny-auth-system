from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from app.controllers.instructor_controllers import InstructorController,InstructorResponse,InstructorCreate

db = Database()
instructor_controller = InstructorController(db)
auth_controller = AuthController(db)

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
    dependencies=[Depends(auth_controller.verify_token)]
)

@router.post("/", response_model=InstructorResponse)
def create_instructor(instructor: InstructorCreate):
    created, error = instructor_controller.create_instructor_logic(instructor)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return created  # This must be the processed dict with id string, no _id ObjectId

@router.get("/")
def get_instructors():
    return instructor_controller.get_all_instructors()

@router.get("/{instructor_id}")
def get_instructor(instructor_id: str):
    instructor = instructor_controller.get_instructor_by_id(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.put("/{instructor_id}")
def update_instructor(instructor_id: str, instructor: InstructorCreate):
    matched_count = instructor_controller.update_instructor_by_id(instructor_id, instructor)
    if matched_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor updated successfully"}

@router.delete("/{instructor_id}")
def delete_instructor(instructor_id: str):
    deleted_count = instructor_controller.delete_instructor_by_id(instructor_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor deleted successfully"}
