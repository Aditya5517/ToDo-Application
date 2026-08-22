from fastapi import FastAPI

from src.routes.routes import router as home_router
from src.routes.auth_routes import router as auth_router
from src.routes.user_routes import router as user_router
from src.routes.project_routes import router as project_router
from src.routes.task_list_routes import router as task_list_router
from src.routes.task_routes import router as task_router 


app = FastAPI(
    title="TODO Task Management API",
    description=(
        "Full-fledged FastAPI and "
        "PostgreSQL task management system"
    ),
    version="2.0.0"
)


app.include_router(auth_router)

app.include_router(user_router)

app.include_router(project_router)

app.include_router(task_list_router)

app.include_router(task_router)

app.include_router(home_router)