
import os
import secrets

from flask import (
    Blueprint,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from sqlalchemy import or_

from app import db, login_manager
from app.models import User

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------- ROLE-BASED REDIRECTION ----------
def redirect_user():
    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))

    return redirect(url_for("dashboard"))


# ---------- REGISTER ----------
@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect_user()

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("auth.register"))

        existing_user = db.session.scalar(
            db.select(User).where(
                or_(User.username == username, User.email == email)
            )
        )

        if existing_user:
            flash("Username or email already exists.", "error")
            return redirect(url_for("auth.register"))

        admin_email = os.environ.get(
            "ADMIN_EMAIL", ""
        ).strip().lower()

        role = "admin" if email == admin_email and admin_email else "user"

        user = User(
            username=username,
            email=email,
            role=role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------- LOGIN ----------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect_user()

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if user and user.check_password(password):

            admin_email = os.environ.get(
                "ADMIN_EMAIL", ""
            ).strip().lower()

            if admin_email and user.email.strip().lower() == admin_email:
                if user.role != "admin":
                    user.role = "admin"
                    db.session.commit()

            login_user(user)

            return redirect_user()

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# ---------- LOGOUT ----------
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have logged out successfully.", "success")

    return redirect(url_for("auth.login"))


# ---------- ADMIN PASSWORD RESET ----------
@auth.route("/admin-password-reset", methods=["GET", "POST"])
def admin_password_reset():

    reset_token = os.environ.get("ADMIN_RESET_TOKEN", "")
    admin_email = os.environ.get(
        "ADMIN_EMAIL", ""
    ).strip().lower()

    if not reset_token or not admin_email:
        abort(404)

    if request.method == "POST":

        entered_token = request.form.get("token", "")
        new_password = request.form.get("new_password", "")

        if not secrets.compare_digest(entered_token, reset_token):
            abort(403)

        if len(new_password) < 8:
            return (
                "Password must contain at least 8 characters.",
                400
            )

        user = db.session.scalar(
            db.select(User).where(User.email == admin_email)
        )

        if not user:
            return "Admin account not found.", 404

        user.set_password(new_password)
        user.role = "admin"

        db.session.commit()

        return """
        <h2>Password reset successful!</h2>
        <p>Your admin password has been changed.</p>
        <a href="/login">Go to Login</a>
        """

    return render_template_string("""
        <h2>TrustVault Admin Password Reset</h2>

        <form method="POST">

            <label>Reset Token:</label><br>
            <input type="password" name="token" required>
            <br><br>

            <label>New Password:</label><br>
            <input type="password"
                   name="new_password"
                   minlength="8"
                   required>
            <br><br>

            <button type="submit">Reset Password</button>

        </form>
    """)
