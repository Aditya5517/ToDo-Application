import json
from utils.logs import logger

def load_tasks():
    try:
        with open("task.json","r") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.warning("task.json not found. Created empty task list.")
        return []
    except json.JSONDecodeError:
        logger.error("task.json contains invalid JSON.")
        return []

def save_tasks(tasks):
    try:
        with open("task.json","w") as file:
            json.dump(tasks,file,indent=4)
    except PermissionError:
        logger.error("Permission denied while saving task.json.")
        print("Unable to save file.")

def load_archive():
    try:
        with open("archive.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
            logger.warning("task.json not found. Created empty task list.")
            return []
    except json.JSONDecodeError:
        logger.error("task.json contains invalid JSON.")
        return []

def save_archive(tasks):
    try:
        with open("archive.json", "w") as file:
            json.dump(tasks, file, indent=4)
    except PermissionError:
        logger.error("Permission denied while saving task.json.")
        print("Unable to save archive.")