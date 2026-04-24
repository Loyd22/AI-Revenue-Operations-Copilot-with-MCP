# Deal model.
# This represents a sales opportunity tied to an account.

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_mixins import TimestampMixin


class Deal(Base, TimestampMixin):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    owner_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    stage_id: Mapped[int | None] = mapped_column(ForeignKey("deal_stages.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open", nullable=False)
    risk_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expected_close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    account = relationship("Account", back_populates="deals")
    owner = relationship("User", back_populates="owned_deals")
    stage = relationship("DealStage", back_populates="deals")
    activities = relationship("Activity", back_populates="deal", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="deal", cascade="all, delete-orphan")