# Account model.
# This represents a customer company/account in the CRM.

from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_mixins import TimestampMixin


class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    health_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    renewal_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    owner_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    # Relationship: account owner
    owner = relationship("User", back_populates="owned_accounts")

    # Relationship: one account can have many contacts, deals, activities, and notes
    contacts = relationship("Contact", back_populates="account", cascade="all, delete-orphan")
    deals = relationship("Deal", back_populates="account", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="account", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="account", cascade="all, delete-orphan")