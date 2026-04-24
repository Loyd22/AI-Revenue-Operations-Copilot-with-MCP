# Activity model.
# This stores meetings, calls, emails, and other account/deal activities.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_mixins import TimestampMixin


class Activity(Base, TimestampMixin):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    deal_id: Mapped[int | None] = mapped_column(ForeignKey("deals.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    subject: Mapped[str] = mapped_column(String(150), nullable=False)
    activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="completed", nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    account = relationship("Account", back_populates="activities")
    deal = relationship("Deal", back_populates="activities")
    user = relationship("User", back_populates="activities")