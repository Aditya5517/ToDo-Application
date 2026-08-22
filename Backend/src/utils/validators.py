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

def valid_role(role):
    allowed = ["admin", "user"]

    if role in allowed:
        return True

    return False

def valid_phone(phone):

    phone = phone.strip()

    if not phone.isdigit():
        return False

    if len(phone) != 10:
        return False

    return True

def password_errors(password):

    errors = []

    if len(password) < 8:
        errors.append(
            "Password must contain at least 8 characters."
        )

    if not any(char.isupper() for char in password):
        errors.append(
            "Password must contain at least one uppercase letter."
        )

    if not any(char.islower() for char in password):
        errors.append(
            "Password must contain at least one lowercase letter."
        )

    if not any(char.isdigit() for char in password):
        errors.append(
            "Password must contain at least one number."
        )

    return errors