def valid_title(title):
    title = title.strip()
    if title == "":
        return False
    if title.isdigit():
        return False
    if not any(char.isalpha() for char in title):
        return False
    return True

def valid_priority(priority):
    allowed = ["High", "Medium", "Low"]
    if priority in allowed:
        return True
    return False

def valid_status(status):
    allowed = [
        "Pending",
        "In Progress",
        "Completed"
    ]
    if status in allowed:
        return True
    return False

