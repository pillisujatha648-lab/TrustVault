
import os
import uuid
from io import BytesIO

from cryptography.exceptions import InvalidTag

from flask import (
    Blueprint, request, redirect,
    url_for, flash, current_app, send_file, abort
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models import Document, DocumentPermission, User
from app.audit import record_audit
from app.permissions import can_access_document
from app.encryption import encrypt_file, decrypt_file


documents = Blueprint("documents", __name__)

ALLOWED_EXTENSIONS = {"pdf", "txt", "docx"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ---------- UPLOAD DOCUMENT ----------

@documents.route("/upload", methods=["POST"])
@login_required
def upload_document():

    file = request.files.get("document")

    if not file or file.filename == "":
        flash("Please select a document.", "error")
        return redirect(url_for("dashboard"))

    if not allowed_file(file.filename):
        flash("Only PDF, TXT and DOCX files are allowed.", "error")
        return redirect(url_for("dashboard"))

    original_name = secure_filename(file.filename)

    if not original_name:
        flash("Invalid filename.", "error")
        return redirect(url_for("dashboard"))

    file_data = file.read()

    if not file_data:
        flash("The selected file is empty.", "error")
        return redirect(url_for("dashboard"))

    encrypted_data = encrypt_file(file_data)

    stored_name = f"{uuid.uuid4().hex}.encrypted"

    storage_path = os.path.join(
        current_app.config["PRIVATE_STORAGE"],
        stored_name
    )

    os.makedirs(current_app.config["PRIVATE_STORAGE"], exist_ok=True)

    with open(storage_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    document = Document(
        title=os.path.splitext(original_name)[0],
        original_filename=original_name,
        stored_filename=stored_name,
        owner_id=current_user.id
    )

    db.session.add(document)
    db.session.commit()

    record_audit(document.id, "UPLOAD", "SUCCESS")
    db.session.commit()

    flash("Document encrypted and uploaded successfully!", "success")

    return redirect(url_for("dashboard"))


# ---------- DOWNLOAD DOCUMENT ----------

@documents.route("/download/<int:document_id>")
@login_required
def download_document(document_id):

    document = db.session.get(Document, document_id)

    if not document:
        abort(404)

    if not can_access_document(document, current_user, "view"):
        record_audit(document.id, "DOWNLOAD", "DENIED")
        db.session.commit()
        abort(403)

    storage_path = os.path.join(
        current_app.config["PRIVATE_STORAGE"],
        document.stored_filename
    )

    if not os.path.isfile(storage_path):
        abort(404)

    with open(storage_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        decrypted_data = decrypt_file(encrypted_data)

    except (InvalidTag, ValueError):
        record_audit(document.id, "DOWNLOAD", "DECRYPTION_FAILED")
        db.session.commit()
        abort(500)

    record_audit(document.id, "DOWNLOAD", "SUCCESS")
    db.session.commit()

    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=document.original_filename
    )


# ---------- SHARE DOCUMENT ----------

@documents.route("/share/<int:document_id>", methods=["POST"])
@login_required
def share_document(document_id):

    document = db.session.get(Document, document_id)

    if not document:
        abort(404)

    if document.owner_id != current_user.id:
        abort(403)

    email = request.form.get("email", "").strip().lower()
    permission_type = request.form.get("permission", "").strip().lower()

    if permission_type not in ["viewer", "editor"]:
        flash("Invalid permission selected.", "error")
        return redirect(url_for("dashboard"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User with this email does not exist.", "error")
        return redirect(url_for("dashboard"))

    if user.id == current_user.id:
        flash("You cannot share a document with yourself.", "error")
        return redirect(url_for("dashboard"))

    existing_permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=user.id
    ).first()

    if existing_permission:
        existing_permission.permission = permission_type
    else:
        new_permission = DocumentPermission(
            document_id=document.id,
            user_id=user.id,
            permission=permission_type
        )
        db.session.add(new_permission)

    db.session.commit()

    record_audit(document.id, "SHARE", "SUCCESS")
    db.session.commit()

    flash("Document shared successfully!", "success")

    return redirect(url_for("dashboard"))


# ---------- REVOKE DOCUMENT ACCESS ----------

@documents.route("/revoke/<int:document_id>", methods=["POST"])
@login_required
def revoke_document_access(document_id):

    document = db.session.get(Document, document_id)

    if not document:
        abort(404)

    # Only the document owner can revoke access
    if document.owner_id != current_user.id:
        abort(403)

    email = request.form.get("email", "").strip().lower()

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.", "error")
        return redirect(url_for("dashboard"))

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=user.id
    ).first()

    if not permission:
        flash("This user does not have access to the document.", "error")
        return redirect(url_for("dashboard"))

    db.session.delete(permission)
    db.session.commit()

    record_audit(document.id, "REVOKE_ACCESS", "SUCCESS")
    db.session.commit()

    flash("Document access revoked successfully!", "success")

    return redirect(url_for("dashboard"))
