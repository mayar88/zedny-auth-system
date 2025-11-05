from app.core.database import Database
from app.models.session_model import Session, SessionResponse
from app.controllers.instructor_controllers import InstructorController
from app.controllers.user_controllers import UserController
from bson import ObjectId



class SessionController:
    def __init__(self, db: Database):
        self.sessions_collection = db.sessions
        self.instructor_controller = InstructorController(db)
        self.user_controller = UserController(db)


    def normalize_entity(self, entity):
        if entity is None:
            return None

        if hasattr(entity, "model_dump"):
            d = entity.model_dump(by_alias=True)
        else:
            d = dict(entity)

        # Convert 'id' to '_id' if needed
        if "id" in d and "_id" not in d:
            d["_id"] = d.pop("id")

        # Ensure _id is string
        if "_id" in d and not isinstance(d["_id"], str):
            d["_id"] = str(d["_id"])

        return d

    def create_session(self, session: Session):
        result = self.sessions_collection.insert_one(session.dict(by_alias=True))
        created = self.sessions_collection.find_one({"_id": result.inserted_id})
        if not created:
            return None

        instructor_obj = self.instructor_controller.get_instructor_by_id(created["instructor_id"])
        user_obj = self.user_controller.get_user_by_id(created["user_id"])

        instructor = self.normalize_entity(instructor_obj)
        user = self.normalize_entity(user_obj)

        created["_id"] = str(created["_id"])
        created["id"] = created["_id"]
        created["instructor"] = instructor
        created["user"] = user

        created.pop("instructor_id", None)
        created.pop("user_id", None)

        return SessionResponse.model_validate(created)

    def get_sessions(self):
        sessions = list(self.sessions_collection.find())
        result = []

        for session in sessions:
            session["_id"] = str(session["_id"])
            session["id"] = session["_id"]

            instructor_obj = self.instructor_controller.get_instructor_by_id(session.get("instructor_id"))
            user_obj = self.user_controller.get_user_by_id(session.get("user_id"))

            session["instructor"] = self.normalize_entity(instructor_obj)
            session["user"] = self.normalize_entity(user_obj)

            session.pop("instructor_id", None)
            session.pop("user_id", None)

            result.append(session)

        return result

    def get_session_by_id(self, session_id: str):
        try:
            oid = ObjectId(session_id)
        except Exception:
            return None
        session = self.sessions_collection.find_one({"_id": oid})
        if session:
            session["_id"] = str(session["_id"])
            session["id"] = session["_id"]

            instructor_obj = self.instructor_controller.get_instructor_by_id(session.get("instructor_id"))
            user_obj = self.user_controller.get_user_by_id(session.get("user_id"))

            session["instructor"] = self.normalize_entity(instructor_obj)
            session["user"] = self.normalize_entity(user_obj)

            session.pop("instructor_id", None)
            session.pop("user_id", None)

        return SessionResponse.model_validate(session) if session else None

    def update_session_by_id(self, session_id: str, session: Session):
        try:
            oid = ObjectId(session_id)
        except Exception:
            return 0
        result = self.sessions_collection.update_one(
            {"_id": oid},
            {"$set": session.dict(exclude={"id"}, by_alias=True)}
        )
        return result.matched_count

    def delete_session_by_id(self, session_id: str):
        try:
            oid = ObjectId(session_id)
        except Exception:
            return 0
        result = self.sessions_collection.delete_one({"_id": oid})
        return result.deleted_count

    db = Database()
    def get_session_from_db(self,session_id: str):
        try:
            oid = ObjectId(session_id)
        except Exception:
            return None

        session = self.db.sessions.find_one({"_id": oid})
        if session:
            session["id"] = str(session["_id"])  # convert ObjectId to string
        return session
