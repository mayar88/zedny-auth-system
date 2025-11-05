from fastapi import FastAPI, Depends,Request
from app.api.user_routes import router as user_router
from app.api.instructor_routes import router as instructor_router
from app.api.session_routes import router as session_router
from app.api.auth_routes import router as auth_router
from app.controllers.auth_controllers import AuthController
from app.core.database import Database
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    PermissionDenied,
    AuthenticationFailed,
    ResourceNotFound,
    InvalidOperation,
    DatabaseError,
)

db = Database()
auth_controller = AuthController(db)


app = FastAPI()

# Register routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(instructor_router)
app.include_router(session_router)

@app.get("/protected")
def protected_route(current_user=Depends(auth_controller.verify_token)):
    return {"message": f"Hello user {current_user}"}


@app.exception_handler(PermissionDenied)
async def permission_denied_handler(request: Request, exc: PermissionDenied):
    return JSONResponse(
        status_code=403,
        content={
            "detail": exc.message,
            "role": exc.role,
            "action": exc.action,
            "resource": exc.resource
        }
    )

@app.exception_handler(AuthenticationFailed)
async def authentication_failed_handler(request: Request, exc: AuthenticationFailed):
    return JSONResponse(
        status_code=401,
        content={"detail": "Authentication failed"},
    )

@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"},
    )

@app.exception_handler(InvalidOperation)
async def invalid_operation_handler(request: Request, exc: InvalidOperation):
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid operation"},
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
