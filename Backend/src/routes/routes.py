from fastapi import APIRouter


router = APIRouter(
    tags=["Health"]
)


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@router.get("/")
def home():

    return {
        "message": "TODO Task Management API is running",
        "status": "success"
    }