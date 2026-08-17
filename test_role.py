from src.services.auth_service import require_admin


admin = {
    "id": 1,
    "username": "admin",
    "role": "admin"
}


user = {
    "id": 2,
    "username": "aditya",
    "role": "user"
}


print("Testing admin:")

result = require_admin(admin)

print("Admin allowed:")
print(result)


print("\nTesting normal user:")

result = require_admin(user)

print(result)