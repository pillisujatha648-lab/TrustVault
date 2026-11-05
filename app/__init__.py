
import os

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager, login_required, current_user

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["PRIVATE_STORAGE"], exist_ok=True)
    os.makedirs(
        app.instance_path,
        exist_ok=True
    )

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth
    from app.documents import documents

    app.register_blueprint(auth)
    app.register_blueprint(documents)

    @app.route("/")
    def home():
        from flask import render_template
        return render_template("index.html")

    # ---------- USER DASHBOARD ----------
    @app.route("/dashboard")
    @login_required
    def dashboard():

        from flask import render_template
        from app.models import Document, DocumentPermission

        # Documents owned by the current user
        owned_documents = Document.query.filter_by(
            owner_id=current_user.id
        ).all()

        # Documents shared with the current user
        shared_permissions = DocumentPermission.query.filter_by(
            user_id=current_user.id
        ).all()

        shared_documents = []

        for permission in shared_permissions:
            document = db.session.get(
                Document,
                permission.document_id
            )

            if document:
                shared_documents.append({
                    "document": document,
                    "permission": permission.permission
                })

        return render_template(
            "dashboard.html",
            documents=owned_documents,
            shared_documents=shared_documents
        )

    # ---------- ADMIN DASHBOARD ----------
    @app.route("/admin")
    @login_required
    def admin_dashboard():

        from flask import render_template
        from app.models import Document, User

        # Only admins can access this page
        if current_user.role != "admin":
            abort(403)

        # Get all uploaded documents
        all_documents = Document.query.order_by(
            Document.uploaded_at.desc()
        ).all()

        # Get all registered users
        all_users = User.query.all()

        return render_template(
            "admin_dashboard.html",
            documents=all_documents,
            users=all_users
        )

    # ---------- CREATE DATABASE TABLES ----------
    with app.app_context():
        from app import models
        from app.models import User

        db.create_all()

        admin_email = os.environ.get("ADMIN_EMAIL")

        if admin_email:
            admin_user = User.query.filter_by(
                email=admin_email
            ).first()

            if admin_user:
                admin_user.role = "admin"
                db.session.commit()

    return app
