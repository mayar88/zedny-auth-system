
from fastapi import Depends
from app.core.exceptions import PermissionDenied, AuthenticationFailed,NotFoundException
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from app.controllers.session_controllers import SessionController

db = Database()
auth_controller = AuthController(db)
session_controller = SessionController(db)


def get_current_user(token_data=Depends(auth_controller.verify_token)):
    if not token_data:
        raise AuthenticationFailed()
    return token_data

def require_admin(current_user=Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise PermissionDenied(
            message="Admin privileges are required to access this resource.",
            role=current_user.get("role"),
            action="access",
            resource="admin-only endpoint"
        )
    return current_user

def require_instructor(current_user=Depends(get_current_user)):
    if current_user.get("role") != "instructor":
        raise PermissionDenied(
            message="Instructor privileges are required to access this resource.",
            role=current_user.get("role"),
            action="access",
            resource="instructor-only endpoint"
        )
    return current_user

def require_own_or_admin(user_id: str, current_user=Depends(get_current_user)):
    if current_user.get("role") == "admin":
        return current_user
    if current_user.get("id") != user_id:
        raise PermissionDenied(
            message="You do not have permission to access this resource.",
            role=current_user.get("role"),
            action="access",
            resource=f"user resource with id {user_id}"
        )
    return current_user

def require_own_or_admin_instructor(instructor_id: str, current_user=Depends(get_current_user)):
    if current_user.get("role") == "admin":
        return current_user
    if current_user.get("id") != instructor_id:
        raise PermissionDenied("You do not have permission to access this instructor resource.",
            role=current_user.get("role"),
            action="access",
            resource=f"user resource with id {instructor_id}"
        )
    return current_user

def require_session_owner_or_admin(session_id: str, current_user=Depends(get_current_user)):
    session = session_controller.get_session_by_id(session_id)
    if not session:
        raise NotFoundException("Session not found")
    if current_user.get("role") == "admin":
        return current_user
    if current_user.get("id") not in [session.get("user_id"), session.get("instructor_id")]:
        raise PermissionDenied(
            message="You do not have permission to access this session.",
            role=current_user.get("role"),
            action="access",
            resource=f"session with id {session_id}"
        )

    return current_user

def require_user_or_instructor(current_user=Depends(get_current_user)):
    if current_user.get("role") not in ["user", "instructor"]:
        raise PermissionDenied(
            message="Access allowed only for users or instructors.",
            role=current_user.get("role"),
            action="access",
            resource="restricted resource"
        )
    return current_user
