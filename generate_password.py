from src.utils.security import hash_password


admin_password = hash_password("admin123")
user_password = hash_password("user123")

print("Admin hash:")
print(admin_password)

print()

print("User hash:")
print(user_password)