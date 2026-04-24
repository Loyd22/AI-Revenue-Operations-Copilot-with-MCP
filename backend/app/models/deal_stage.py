# DealStage model.
# This stores the available sales stages for deals.

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_mixins import TimestampMixin


class DealStage(Base, TimestampMixin):
    __tablename__ = "deal_stages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    stage_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_won: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationship: one stage can have many deals
    deals = relationship("Deal", back_populates="stage")