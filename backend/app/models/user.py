# User model.
# This represents a person who can log in and use the system.

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    # Relationship: user belongs to one role
    role = relationship("Role", back_populates="users")

    # Relationship: one user can own many accounts and deals
    owned_accounts = relationship("Account", back_populates="owner")
    owned_deals = relationship("Deal", back_populates="owner")

    # Relationship: one user can create many activities, notes, documents, and audit logs
    activities = relationship("Activity", back_populates="user")
    notes = relationship("Note", back_populates="user")
    documents = relationship("Document", back_populates="uploaded_by")
    audit_logs = relationship("AuditLog", back_populates="user")