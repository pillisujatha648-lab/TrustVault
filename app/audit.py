
from flask import request
from flask_login import current_user

from app import db
from app.models import AuditLog


def record_audit(document_id, action, result):

    user_id = None

    if current_user.is_authenticated:
        user_id = current_user.id

    log = AuditLog(
        user_id=user_id,
        document_id=document_id,
        action=action,
        result=result,
        ip_address=request.remote_addr
    )

    db.session.add(log)
    db.session.flush()
