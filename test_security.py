from src.utils.security import (
    hash_password,
    verify_password
)


password = "admin123"

hashed_password = hash_password(password)

print("Original password:")
print(password)

print("\nHashed password:")
print(hashed_password)

print("\nCorrect password:")
print(
    verify_password(
        "admin123",
        hashed_password
    )
)

print("\nWrong password:")
print(
    verify_password(
        "wrongpassword",
        hashed_password
    )
)