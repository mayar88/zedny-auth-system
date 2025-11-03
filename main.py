from fastapi import FastAPI, Depends
from app.api.user_routes import router as user_router
from app.api.instructor_routes import router as instructor_router
from app.api.session_routes import router as session_router
from app.api.auth_routes import router as auth_router
from app.controllers.auth_controllers import AuthController
from app.core.database import Database

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
