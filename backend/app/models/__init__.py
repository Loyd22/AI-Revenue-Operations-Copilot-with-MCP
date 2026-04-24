# Import all models here so SQLAlchemy and Alembic can see them.

from app.models.role import Role
from app.models.user import User
from app.models.account import Account
from app.models.contact import Contact
from app.models.deal_stage import DealStage
from app.models.deal import Deal
from app.models.activity import Activity
from app.models.note import Note
from app.models.document import Document
from app.models.audit_log import AuditLog

__all__ = [
    "Role",
    "User",
    "Account",
    "Contact",
    "DealStage",
    "Deal",
    "Activity",
    "Note",
    "Document",
    "AuditLog",
]