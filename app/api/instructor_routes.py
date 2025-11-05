from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from app.controllers.instructor_controllers import InstructorController,InstructorResponse,InstructorCreate
from app.core.permissions import require_admin, require_instructor, require_own_or_admin_instructor

db = Database()
instructor_controller = InstructorController(db)
auth_controller = AuthController(db)

router = APIRouter(
    prefix="/instructors",
    tags=["Instructors"],
    dependencies=[Depends(auth_controller.verify_token)]
)

@router.post("/", response_model=InstructorResponse ,dependencies=[Depends(require_admin)])
def create_instructor(instructor: InstructorCreate):
    created, error = instructor_controller.create_instructor_logic(instructor)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return created

@router.get("/",dependencies=[Depends(require_admin)])
def get_instructors():
    return instructor_controller.get_all_instructors()

@router.get("/{instructor_id}",dependencies=[Depends(require_own_or_admin_instructor)] )
def get_instructor(instructor_id: str):
    instructor = instructor_controller.get_instructor_by_id(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor

@router.put("/{instructor_id}",dependencies=[Depends(require_own_or_admin_instructor)])
def update_instructor(instructor_id: str, instructor: InstructorCreate):
    matched_count = instructor_controller.update_instructor_by_id(instructor_id, instructor)
    if matched_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor updated successfully"}

@router.delete("/{instructor_id}",dependencies=[Depends(require_admin)])
def delete_instructor(instructor_id: str):
    deleted_count = instructor_controller.delete_instructor_by_id(instructor_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {"message": "Instructor deleted successfully"}

