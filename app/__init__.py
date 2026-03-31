from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from app.config import Config
from app.extensions import db, login_manager
from app.models.user import User
from app.routes.auth_routes import auth_bp
from app.routes.student_routes import student_bp
from app.routes.main_routes import main_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Authentication required."}), 401

        flash(login_manager.login_message, login_manager.login_message_category)
        return redirect(url_for("auth_bp.login"))

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)

    @app.route("/test-500")
    def test_500():
        raise Exception("Test 500 error")

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Resource not found."}), 404
        return render_template("404.html"), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Method not allowed."}), 405
        return render_template("404.html"), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Internal server error."}), 500
        return render_template("404.html"), 500

    with app.app_context():
        db.create_all()

    return app
