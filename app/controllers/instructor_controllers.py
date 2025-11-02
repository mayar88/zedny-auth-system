from app.models.instructor_model import InstructorCreate
from app.core.database import instructors_collection
from app.models.instructor_model import InstructorResponse
from bson import ObjectId

class InstructorController:
    def __init__(self):
        self.instructors_collection = instructors_collection

    def create_instructor_logic(self, instructor: InstructorCreate):
        instructor_dict = instructor.dict(by_alias=True)
        if self.instructors_collection.find_one({"name": instructor.name}):
            return None, "Instructor with this name already exists."
        result = self.instructors_collection.insert_one(instructor_dict)
        created = self.instructors_collection.find_one({"_id": result.inserted_id})
        if created:
            # convert ObjectId to string but keep key '_id'
            created['_id'] = str(created['_id'])
        return InstructorResponse.model_validate(created), None

    def get_all_instructors(self):
        instructors = list(self.instructors_collection.find())
        for inst in instructors:
            inst["id"] = str(inst["_id"])  # convert ObjectId to string
            del inst["_id"]
        return instructors

    def get_instructor_by_id(self, instructor_id: str):
        try:
            oid = ObjectId(instructor_id)
        except Exception:
            return None  # invalid ObjectId format

        instructor = self.instructors_collection.find_one({"_id": oid})
        if instructor:
            instructor["_id"] = str(instructor["_id"])
            # ✅ Return as Pydantic model, not dict
            return InstructorResponse.model_validate(instructor)
        return None

        instructor = self.instructors_collection.find_one({"_id": oid})
        if instructor:
            instructor["id"] = str(instructor["_id"])
            del instructor["_id"]
        return instructor

    def update_instructor_by_id(self, instructor_id: str, instructor: InstructorCreate):
        try:
            oid = ObjectId(instructor_id)
        except Exception:
            return 0  # invalid ObjectId format

        result = self.instructors_collection.update_one(
            {"_id": oid},
            {"$set": instructor.dict(exclude={"id"}, by_alias=True)}
        )
        return result.matched_count

    def delete_instructor_by_id(self, instructor_id: str):
        try:
            oid = ObjectId(instructor_id)
        except Exception:
            return 0  # invalid ObjectId format

        result = self.instructors_collection.delete_one({"_id": oid})
        return result.deleted_count
