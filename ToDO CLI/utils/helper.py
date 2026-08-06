def generate_id(tasks):
    """
    This function helps us in generating the task id automatically by looking to the last id
    """
    if not tasks:
        return 1
    else:
        last_task=tasks[-1]
        return last_task["id"]+1


def sanitize_string(text):
    """
    Removes leading/trailing spaces and converts
    multiple spaces into a single space.
    """
    return " ".join(text.strip().split())


def normalize_priority(priority):
    """
    This function helps in making the priority look consistent
    """
    priority = sanitize_string(priority).lower()
    mapping = {
        "high": "High",
        "medium": "Medium",
        "low": "Low"
    }
    return mapping.get(priority)


def normalize_status(status):
    """
    This function help in makinng the status look consistent
    """
    status = sanitize_string(status).lower()
    mapping = {
        "pending": "Pending",
        "in progress": "In Progress",
        "completed": "Completed"
    }
    return mapping.get(status)


def safe_int(value):
    """
    This function is used to check that the input is a valid integer or not 
    """
    try:
        return int(value)
    except ValueError:
        return None


def is_empty(text):
    """
    This function helps us to deal with the empty input 
    """
    return sanitize_string(text) == ""


def find_task_by_id(tasks, task_id):
    """
    This function helps in finding the task according to the provided task id 
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def task_exists(tasks, title):
    """
    Checks whether a task with the same title already exists.
    """
    title = sanitize_string(title).lower()
    for task in tasks:
        if sanitize_string(task["title"]).lower() == title:
            return True
    return False


def print_task(task):
    """
    Prints a task in a formatted way.
    """
    print(f"ID       : {task['id']}")
    print(f"Title    : {task['title']}")
    print(f"Priority : {task['priority']}")
    print(f"Status   : {task['status']}")
    print("-" * 35)


def find_task_by_title(tasks, title):
    """
    Find a task by its title.
    """
    title = sanitize_string(title).lower()
    for task in tasks:
        if task["title"].lower() == title:
            return task
    return None