from app.core.database import users_collection
from app.models.user_model import UserCreate, UserResponse
from passlib.context import CryptContext
from bson import ObjectId

class UserController:
    def __init__(self):
        self.users_collection = users_collection
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, user: UserCreate):
        if self.users_collection.find_one({"email": user.email}):
            return None, f"User with email {user.email} already exists"

        user_dict = user.dict()
        user_dict["password"] = self.pwd_context.hash(user.password)
        result = self.users_collection.insert_one(user_dict)

        created = self.users_collection.find_one({"_id": result.inserted_id})
        if created:
            created["_id"] = str(created["_id"])
        return UserResponse.model_validate(created), None

    def get_all_users(self):
        users = list(self.users_collection.find())
        for u in users:
            u["_id"] = str(u["_id"])
        return [UserResponse.model_validate(u) for u in users]

    def get_user_by_id(self, user_id: str):
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None

        user = self.users_collection.find_one({"_id": oid})
        if user:
            user["_id"] = str(user["_id"])
        return UserResponse.model_validate(user) if user else None

    def update_user_by_id(self, user_id: str, user: UserCreate):
        try:
            oid = ObjectId(user_id)
        except Exception:
            return 0

        update_dict = user.dict(exclude={"password"})  # Optionally exclude password update here
        # Or hash password if you want to allow password update
        if user.password:
            update_dict["password"] = self.pwd_context.hash(user.password)

        result = self.users_collection.update_one({"_id": oid}, {"$set": update_dict})
        return result.matched_count

    def delete_user_by_id(self, user_id: str):
        try:
            oid = ObjectId(user_id)
        except Exception:
            return 0
        result = self.users_collection.delete_one({"_id": oid})
        return result.deleted_count
