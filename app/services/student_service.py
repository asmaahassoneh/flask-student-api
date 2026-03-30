from app.extensions import db
from app.models.student import Student
from app.utils.validators import (
    normalize_email,
    normalize_student_id,
    normalize_text,
)


def get_all_students():
    students = Student.query.order_by(Student.name.asc()).all()
    return [student.to_dict() for student in students]


def get_student_by_student_id(student_id):
    normalized_id = normalize_student_id(student_id)
    return Student.query.filter_by(student_id=normalized_id).first()


def create_student(data):
    student = Student(
        name=normalize_text(data["name"]),
        student_id=normalize_student_id(data["student_id"]),
        email=normalize_email(data["email"]),
        age=data["age"],
        major=normalize_text(data["major"]),
    )
    db.session.add(student)
    db.session.commit()
    return student


def update_student(student, data):
    if "name" in data:
        student.name = normalize_text(data["name"])

    if "student_id" in data:
        student.student_id = normalize_student_id(data["student_id"])

    if "email" in data:
        student.email = normalize_email(data["email"])

    if "age" in data:
        student.age = data["age"]

    if "major" in data:
        student.major = normalize_text(data["major"])

    db.session.commit()
    return student


def delete_student(student):
    db.session.delete(student)
    db.session.commit()
