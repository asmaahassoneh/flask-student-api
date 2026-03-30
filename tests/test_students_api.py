from app.extensions import db
from app.models.student import Student


def create_sample_student():
    return Student(
        name="Asmaa Hassoneh",
        student_id="12112458",
        email="asmaa@example.com",
        age=22,
        major="Computer Engineering",
    )


def create_second_student():
    return Student(
        name="Lina Ahmad",
        student_id="12112459",
        email="lina@example.com",
        age=21,
        major="Medicine",
    )


def test_get_all_students_empty(client):
    response = client.get("/api/students")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] == 0
    assert data["data"] == []


def test_get_all_students_with_data(client, app):
    with app.app_context():
        student1 = create_sample_student()
        student2 = create_second_student()
        db.session.add_all([student1, student2])
        db.session.commit()

    response = client.get("/api/students")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] == 2
    assert len(data["data"]) == 2


def test_create_student_success(client):
    payload = {
        "name": "Asmaa Hassoneh",
        "student_id": "12112458",
        "email": "asmaa@example.com",
        "age": 22,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Student created successfully."
    assert data["data"]["name"] == "Asmaa Hassoneh"
    assert data["data"]["student_id"] == "12112458"
    assert data["data"]["email"] == "asmaa@example.com"


def test_create_student_missing_fields(client):
    payload = {
        "name": "Asmaa Hassoneh",
        "student_id": "12112458",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "Missing required fields" in data["error"]


def test_create_student_empty_name(client):
    payload = {
        "name": "   ",
        "student_id": "12112458",
        "email": "asmaa@example.com",
        "age": 22,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Name is required."


def test_create_student_invalid_student_id_format(client):
    payload = {
        "name": "Asmaa Hassoneh",
        "student_id": "12-112458",
        "email": "asmaa@example.com",
        "age": 22,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Student ID must contain only letters and numbers."


def test_create_student_invalid_email(client):
    payload = {
        "name": "Asmaa Hassoneh",
        "student_id": "12112458",
        "email": "wrong-email",
        "age": 22,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Email is not valid."


def test_create_student_duplicate_email(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "name": "Another Student",
        "student_id": "99999999",
        "email": "asmaa@example.com",
        "age": 23,
        "major": "Medicine",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Email already exists."


def test_create_student_invalid_age_type(client):
    payload = {
        "name": "Asmaa Hassoneh",
        "student_id": "12112458",
        "email": "asmaa@example.com",
        "age": "22",
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Age must be an integer."


def test_create_student_age_too_small(client):
    payload = {
        "name": "Young Student",
        "student_id": "12112000",
        "email": "young@example.com",
        "age": 10,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Age must be between 15 and 100."


def test_create_student_age_too_large(client):
    payload = {
        "name": "Old Student",
        "student_id": "12112001",
        "email": "old@example.com",
        "age": 120,
        "major": "Computer Engineering",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Age must be between 15 and 100."


def test_create_student_duplicate_student_id(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "name": "Another Student",
        "student_id": "12112458",
        "email": "another@example.com",
        "age": 23,
        "major": "Medicine",
    }

    response = client.post("/api/students", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Student ID already exists."


def test_get_student_success(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    response = client.get("/api/students/12112458")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == "Asmaa Hassoneh"


def test_get_student_case_insensitive_id(client, app):
    with app.app_context():
        student = Student(
            name="Asmaa Hassoneh",
            student_id="AB123",
            email="asmaa@example.com",
            age=22,
            major="Computer Engineering",
        )
        db.session.add(student)
        db.session.commit()

    response = client.get("/api/students/ab123")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["student_id"] == "AB123"


def test_get_student_not_found(client):
    response = client.get("/api/students/99999999")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Student not found."


def test_update_student_success(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "name": "Asmaa Updated",
        "major": "Software Engineering",
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == "Asmaa Updated"
    assert data["data"]["major"] == "Software Engineering"


def test_update_student_email_success(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "email": "newasmaa@example.com",
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["email"] == "newasmaa@example.com"


def test_update_student_duplicate_email(client, app):
    with app.app_context():
        student1 = create_sample_student()
        student2 = create_second_student()
        db.session.add_all([student1, student2])
        db.session.commit()

    payload = {
        "email": "lina@example.com",
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Email already exists."


def test_update_student_duplicate_student_id(client, app):
    with app.app_context():
        student1 = create_sample_student()
        student2 = create_second_student()
        db.session.add_all([student1, student2])
        db.session.commit()

    payload = {
        "student_id": "12112459",
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Student ID already exists."


def test_update_student_invalid_email(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "email": "bad-email",
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Email is not valid."


def test_update_student_invalid_age(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    payload = {
        "age": 200,
    }

    response = client.put("/api/students/12112458", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Age must be between 15 and 100."


def test_update_student_empty_json_is_allowed(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    response = client.put("/api/students/12112458", json={})

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == "Asmaa Hassoneh"


def test_update_student_not_found(client):
    payload = {"name": "Updated Name"}

    response = client.put("/api/students/00000000", json=payload)

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Student not found."


def test_delete_student_success(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    response = client.delete("/api/students/12112458")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Student deleted successfully."

    with app.app_context():
        student = Student.query.filter_by(student_id="12112458").first()
        assert student is None


def test_delete_student_not_found(client):
    response = client.delete("/api/students/00000000")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Student not found."


def test_invalid_json_body(client):
    response = client.post(
        "/api/students",
        data="not-json",
        content_type="text/plain",
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Request body must be valid JSON."


def test_invalid_json_body_on_put(client, app):
    with app.app_context():
        student = create_sample_student()
        db.session.add(student)
        db.session.commit()

    response = client.put(
        "/api/students/12112458",
        data="not-json",
        content_type="text/plain",
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Request body must be valid JSON."


def test_unknown_route_returns_404(client):
    response = client.get("/api/unknown")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Resource not found."


def test_method_not_allowed(client):
    response = client.patch("/api/students")

    assert response.status_code == 405
    data = response.get_json()
    assert data["error"] == "Method not allowed."


def test_internal_server_error_handler(client, monkeypatch):
    def broken_query():
        raise Exception("Unexpected failure")

    monkeypatch.setattr(
        "app.routes.student_routes.get_all_students",
        broken_query,
    )

    response = client.get("/api/students")
    assert response.status_code == 500
    data = response.get_json()
    assert data["success"] is False
    assert data["error"] == "Internal server error."
