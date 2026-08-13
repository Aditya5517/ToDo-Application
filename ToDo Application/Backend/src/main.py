from fastapi import FastAPI
from src.routes.routes import router


app = FastAPI(
    title="TODO CLI Manager API",
    description="API for managing TODO tasks",
    version="1.0.0"
)

app.include_router(router)