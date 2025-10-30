from app.models.instructor_model import Instructor
from app.core.database import instructors_collection
from bson import ObjectId


# Create a new instructor
def create_instructor_logic(instructor: Instructor):
    # Check uniqueness by name
    if instructors_collection.find_one({"name": instructor.name}):
        return None, "Instructor with this name already exists."

    result = instructors_collection.insert_one(instructor.dict(by_alias=True))
    instructor.id = str(result.inserted_id)
    return instructor, None


# Get all instructors
def get_all_instructors():
    return list(instructors_collection.find({}, {"_id": 0}))


# Get a single instructor by MongoDB _id
def get_instructor_by_id(instructor_id: str):
    return instructors_collection.find_one({"_id": ObjectId(instructor_id)}, {"_id": 0})


# Update an instructor by MongoDB _id
def update_instructor_by_id(instructor_id: str, instructor: Instructor):
    result = instructors_collection.update_one(
        {"_id": ObjectId(instructor_id)},
        {"$set": instructor.dict(exclude={"id"}, by_alias=True)}
    )
    return result.matched_count


# Delete an instructor by MongoDB _id
def delete_instructor_by_id(instructor_id: str):
    result = instructors_collection.delete_one({"_id": ObjectId(instructor_id)})
    return result.deleted_count
