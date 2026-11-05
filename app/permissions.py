
from app.models import DocumentPermission


def can_access_document(document, user, action="view"):

    # Document owner has full access
    if document.owner_id == user.id:
        return True

    # Find the user's permission for this document
    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=user.id
    ).first()

    # No permission means no access
    if permission is None:
        return False

    # Viewer can only view documents
    if action == "view":
        return permission.permission in ["viewer", "editor"]

    # Editor can edit documents
    if action == "edit":
        return permission.permission == "editor"

    # Deny all other actions by default
    return False
