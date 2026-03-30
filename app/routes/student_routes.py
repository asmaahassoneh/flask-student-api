from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.models.student import Student
from app.services.student_service import (
    create_student,
    delete_student,
    get_all_students,
    get_student_by_student_id,
    update_student,
)
from app.utils.validators import (
    normalize_email,
    normalize_student_id,
    validate_student_payload,
)

student_bp = Blueprint("student_bp", __name__, url_prefix="/api/students")


@student_bp.route("", methods=["GET"])
def list_students():
    students = get_all_students()
    return (
        jsonify(
            {
                "success": True,
                "count": len(students),
                "data": students,
            }
        ),
        200,
    )


@student_bp.route("/<student_id>", methods=["GET"])
def get_student(student_id):
    student = get_student_by_student_id(student_id)

    if student is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Student not found.",
                }
            ),
            404,
        )

    return (
        jsonify(
            {
                "success": True,
                "data": student.to_dict(),
            }
        ),
        200,
    )


@student_bp.route("", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    error = validate_student_payload(data)
    if error:
        return jsonify({"success": False, "error": error}), 400

    existing_student_id = Student.query.filter_by(
        student_id=normalize_student_id(data["student_id"])
    ).first()
    if existing_student_id:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Student ID already exists.",
                }
            ),
            400,
        )

    existing_email = Student.query.filter_by(
        email=normalize_email(data["email"])
    ).first()
    if existing_email:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Email already exists.",
                }
            ),
            400,
        )

    try:
        student = create_student(data)
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Student created successfully.",
                    "data": student.to_dict(),
                }
            ),
            201,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Database integrity error.",
                }
            ),
            400,
        )


@student_bp.route("/<student_id>", methods=["PUT"])
def edit_student(student_id):
    student = get_student_by_student_id(student_id)

    if student is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Student not found.",
                }
            ),
            404,
        )

    data = request.get_json(silent=True)

    error = validate_student_payload(data, partial=True)
    if error:
        return jsonify({"success": False, "error": error}), 400

    if "student_id" in data:
        new_student_id = normalize_student_id(data["student_id"])
        existing_student = Student.query.filter_by(student_id=new_student_id).first()
        if existing_student and existing_student.id != student.id:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Student ID already exists.",
                    }
                ),
                400,
            )

    if "email" in data:
        new_email = normalize_email(data["email"])
        existing_email = Student.query.filter_by(email=new_email).first()
        if existing_email and existing_email.id != student.id:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Email already exists.",
                    }
                ),
                400,
            )

    try:
        updated_student = update_student(student, data)
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Student updated successfully.",
                    "data": updated_student.to_dict(),
                }
            ),
            200,
        )
    except IntegrityError:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Database integrity error.",
                }
            ),
            400,
        )


@student_bp.route("/<student_id>", methods=["DELETE"])
def remove_student(student_id):
    student = get_student_by_student_id(student_id)

    if student is None:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Student not found.",
                }
            ),
            404,
        )

    delete_student(student)
    return (
        jsonify(
            {
                "success": True,
                "message": "Student deleted successfully.",
            }
        ),
        200,
    )
