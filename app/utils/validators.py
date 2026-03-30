import re

REQUIRED_FIELDS = ["name", "student_id", "email", "age", "major"]


def normalize_text(value):
    return value.strip() if isinstance(value, str) else value


def normalize_student_id(student_id):
    if not isinstance(student_id, str):
        return student_id
    return student_id.strip().upper()


def normalize_email(email):
    if not isinstance(email, str):
        return email
    return email.strip().lower()


def is_valid_email(email):
    if not isinstance(email, str):
        return False

    pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    return re.match(pattern, email) is not None


def validate_student_payload(data, partial=False):
    if not isinstance(data, dict):
        return "Request body must be valid JSON."

    if not partial:
        missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}."

    if "name" in data:
        name = normalize_text(data.get("name"))
        if not name:
            return "Name is required."

    if "student_id" in data:
        student_id = normalize_student_id(data.get("student_id"))
        if not student_id:
            return "Student ID is required."
        if not student_id.isalnum():
            return "Student ID must contain only letters and numbers."

    if "email" in data:
        email = normalize_email(data.get("email"))
        if not email:
            return "Email is required."
        if not is_valid_email(email):
            return "Email is not valid."

    if "age" in data:
        age = data.get("age")
        if not isinstance(age, int):
            return "Age must be an integer."
        if age < 15 or age > 100:
            return "Age must be between 15 and 100."

    if "major" in data:
        major = normalize_text(data.get("major"))
        if not major:
            return "Major is required."

    return None
