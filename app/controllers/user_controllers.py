from app.core.database import users_collection
from app.models.user_model import User
from passlib.context import CryptContext
from bson import ObjectId

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create a new user
def create_user_logic(user: User):
    # Check if email already exists
    if users_collection.find_one({"email": user.email}):
        return None, "User already exists"

    # Hash the password
    user.password = pwd_context.hash(user.password)

    # Insert into MongoDB
    result = users_collection.insert_one(user.dict(by_alias=True))
    user.id = str(result.inserted_id)
    return user, None


# Get all users
def get_all_users():
    return list(users_collection.find({}, {"_id": 0}))


# Get a single user by MongoDB _id
def get_user_by_id(user_id: str):
    return users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0})


# Update user
def update_user_by_id(user_id: str, user: User):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict(exclude={"id"}, by_alias=True)}
    )
    return result.matched_count


# Delete user
def delete_user_by_id(user_id: str):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count
