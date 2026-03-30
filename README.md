# Flask Student Portal with Data Base

A modular Flask web application for managing students and their enrolled courses, built using **Flask, SQLAlchemy,** and **Blueprint architecture.**

## Features

- Add, edit, and delete students
- Enroll students in multiple courses (many-to-many)
- View all students and their course count
- View detailed student information
- Input validation and error handling
- Flash messages for user feedback
- Clean UI with reusable templates
- Modular Flask structure using Blueprints
- Application factory pattern (create_app)
- SQLite database with SQLAlchemy ORM
- Seed script for demo data

## 🧱 Tech Stack

- Backend: Flask, Flask-SQLAlchemy, Flask-Migrate
- Database: SQLite
- Frontend: HTML, CSS (Jinja2 templates)
- Architecture: Blueprint-based modular structure

## Project Structure

```text
flask-student-portal-v2/
│
├── app/
│   ├── __init__.py          
│   ├── extensions.py        
│   │
│   ├── models/
│   │   ├── student.py
│   │   └── course.py
│   │
│   ├── routes/
│   │   └── student_routes.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── add_student.html
│   │   ├── edit_student.html
│   │   ├── students.html
│   │   ├── student_details.html
│   │   └── 404.html
│   │
│   └── static/
│       └── style.css
│
├── config.py
├── seed.py                
├── run.py                
└── README.md
```

---

# ⚙️ Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install flask flask_sqlalchemy flask_migrate
pip install -r requirements.txt
```

---

## ▶️ How to Run
Initialize database
```bash
python seed.py
```
Run the app:

```bash
python run.py
```

Then open:

```
http://127.0.0.1:5000
```

---

Run linting and formatting:

```bash
flake8 .
black .
```

