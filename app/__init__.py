from flask import Flask, jsonify

from app.config import Config
from app.extensions import db
from app.routes.student_routes import student_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.register_blueprint(student_bp)

    @app.route("/")
    def index():
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Flask Student API is running.",
                    "endpoints": {
                        "get_all_students": "/api/students",
                        "get_one_student": "/api/students/<student_id>",
                    },
                }
            ),
            200,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Resource not found.",
                }
            ),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Method not allowed.",
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Internal server error.",
                }
            ),
            500,
        )

    with app.app_context():
        db.create_all()

    return app
