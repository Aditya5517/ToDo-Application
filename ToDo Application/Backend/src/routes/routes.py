from fastapi import APIRouter, HTTPException
from src.routes.models import TaskCreate, TaskUpdate
from src.services.file_handler import (
    load_tasks,
    save_tasks,
    load_archive,
    save_archive,
    load_users,
    save_users
)
from src.routes.models import (
    TaskCreate,
    TaskUpdate,
    LoginRequest,
    LoginResponse,
    UserCreate,
    UserResponse
)
from src.services.user_service import create_user
from src.utils.validators import (
    valid_title,
    valid_priority,
    valid_status,
    valid_phone
)
from src.utils import helper
from src.services.auth_service import authenticate_user
from src.utils.logs import logger
    

router = APIRouter()


# =========================
# HOME
# =========================

@router.get("/")
def home():
    return {
        "message": "TODO CLI Manager API is running"
    }


# =========================
# GET ALL ACTIVE TASKS
# =========================

@router.get("/tasks")
def get_tasks():

    tasks = load_tasks()

    return {
        "tasks": tasks
    }


# =========================
# CREATE TASK
# =========================

@router.post("/tasks")
def create_task(task_data: TaskCreate):

    if not valid_title(task_data.title):
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid task title."
        )

    if not valid_priority(task_data.priority):
        raise HTTPException(
            status_code=400,
            detail="Priority must be High, Medium or Low."
        )

    if not valid_status(task_data.status):
        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, In Progress or Completed."
        )

    tasks = load_tasks()

    if helper.task_exists(tasks, task_data.title):
        raise HTTPException(
            status_code=409,
            detail="Task already exists."
        )

    task_id = helper.generate_id(tasks)

    new_task = {
        "id": task_id,
        "title": helper.sanitize_string(task_data.title),
        "priority": task_data.priority,
        "status": task_data.status
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return {
        "message": "Task created successfully",
        "task": new_task
    }


# =========================
# GET TASK BY ID
# =========================

@router.get("/tasks/{task_id}")
def get_task(task_id: int):

    tasks = load_tasks()

    task = helper.find_task_by_id(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    return {
        "task": task
    }


# =========================
# UPDATE TASK
# =========================

@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate
):

    tasks = load_tasks()

    task = helper.find_task_by_id(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    # Update title
    if task_data.title is not None:

        if not valid_title(task_data.title):
            raise HTTPException(
                status_code=400,
                detail="Please enter a valid task title."
            )

        # Prevent duplicate titles
        if (
            task_data.title.strip().lower()
            != task["title"].strip().lower()
            and helper.task_exists(tasks, task_data.title)
        ):
            raise HTTPException(
                status_code=409,
                detail="Another task with this title already exists."
            )

        task["title"] = helper.sanitize_string(
            task_data.title
        )

    # Update priority
    if task_data.priority is not None:

        if not valid_priority(task_data.priority):
            raise HTTPException(
                status_code=400,
                detail="Priority must be High, Medium or Low."
            )

        task["priority"] = task_data.priority

    # Update status
    if task_data.status is not None:

        if not valid_status(task_data.status):
            raise HTTPException(
                status_code=400,
                detail="Status must be Pending, In Progress or Completed."
            )

        task["status"] = task_data.status

    save_tasks(tasks)

    return {
        "message": "Task updated successfully",
        "task": task
    }


# =========================
# DELETE TASK
# =========================

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    tasks = load_tasks()

    task = helper.find_task_by_id(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    tasks.remove(task)

    save_tasks(tasks)

    return {
        "message": "Task deleted successfully",
        "task": task
    }


# =========================
# DASHBOARD
# =========================

@router.get("/dashboard")
def dashboard():

    tasks = load_tasks()
    archived_tasks = load_archive()

    # Include active + archived tasks
    all_tasks = tasks + archived_tasks

    total = len(all_tasks)

    pending = 0
    in_progress = 0
    completed = 0

    high = 0
    medium = 0
    low = 0

    for task in all_tasks:

        if task["status"] == "Pending":
            pending += 1

        elif task["status"] == "In Progress":
            in_progress += 1

        elif task["status"] == "Completed":
            completed += 1

        if task["priority"] == "High":
            high += 1

        elif task["priority"] == "Medium":
            medium += 1

        elif task["priority"] == "Low":
            low += 1

    completion_rate = (
        completed / total * 100
        if total > 0
        else 0
    )

    return {
        "total_tasks": total,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "high_priority": high,
        "medium_priority": medium,
        "low_priority": low,
        "completion_rate": round(
            completion_rate,
            2
        )
    }


# =========================
# VIEW ARCHIVED TASKS
# =========================

@router.get("/archive")
def get_archive():

    archived_tasks = load_archive()

    return {
        "total_archived": len(archived_tasks),
        "tasks": archived_tasks
    }


# =========================
# ARCHIVE COMPLETED TASKS
# =========================

@router.post("/archive")
def archive_completed_tasks():

    tasks = load_tasks()
    archive = load_archive()

    completed_tasks = [
        task
        for task in tasks
        if task["status"] == "Completed"
    ]

    if not completed_tasks:
        return {
            "message": "No completed tasks to archive.",
            "archived_count": 0
        }

    archive.extend(completed_tasks)

    tasks = [
        task
        for task in tasks
        if task["status"] != "Completed"
    ]

    save_tasks(tasks)
    save_archive(archive)

    return {
        "message": "Completed tasks archived successfully.",
        "archived_count": len(completed_tasks),
        "archived_tasks": completed_tasks
    }

#Get Users
@router.get("/users")
def get_users():

    users = load_users()

    return {
        "users": [
            {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"]
            }
            for user in users
        ]
    }


# =========================
# REGISTER USER
# =========================

@router.post(
    "/auth/register",
    response_model=UserResponse
)
def register_user(user_data: UserCreate):

    if not valid_phone(user_data.phone):

        raise HTTPException(
            status_code=400,
            detail="Phone number must contain exactly 10 digits."
        )

    user, error = create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        phone=user_data.phone
    )

    if error:

        raise HTTPException(
            status_code=409,
            detail=error
        )

    return user


@router.post("/auth/login")
def login_user(login_data: LoginRequest):

    user = authenticate_user(
        username=login_data.username,
        password=login_data.password
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    return {
        "message": "Login successful.",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"],
            "role": user["role"],
            "is_active": user["is_active"]
        }
    }

#Logout
@router.post("/auth/logout")
def logout_user():

    logger.info("User logout Succesfully")

    return {
        "message": "Logout successful."
    }