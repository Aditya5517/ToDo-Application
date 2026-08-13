import json
from src.utils.logs import logger

def load_tasks():
    try:
        with open("file/task.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("task.json not found. Created empty task list.")
        return []
    except json.JSONDecodeError:
        logger.error("task.json contains invalid JSON.")
        return []

def save_tasks(tasks):
    try:
        with open("file/task.json","w") as file:
            json.dump(tasks,file,indent=4)
    except PermissionError:
        logger.error("Permission denied while saving task.json.")
        print("Unable to save file.")

def load_archive():
    try:
        with open("file/archive.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
            logger.warning("task.json not found. Created empty task list.")
            return []
    except json.JSONDecodeError:
        logger.error("task.json contains invalid JSON.")
        return []

def save_archive(tasks):
    try:
        with open("file/archive.json", "w") as file:
            json.dump(tasks, file, indent=4)
    except PermissionError:
        logger.error("Permission denied while saving task.json.")
        print("Unable to save archive.")

def load_users():
    try:
        with open("file/users.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        logger.warning(
            "users.json not found. Returning empty user list."
        )
        return []

    except json.JSONDecodeError:
        logger.error(
            "users.json contains invalid JSON."
        )
        return []

def save_users(users):
    try:
        with open("file/users.json", "w") as file:
            json.dump(users, file, indent=4)

    except PermissionError:
        logger.error(
            "Permission denied while saving users.json."
        )
        print("Unable to save users file.")


