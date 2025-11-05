from enum import Enum

# Define roles using Enum
class UserRole(str, Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    USER = "user"