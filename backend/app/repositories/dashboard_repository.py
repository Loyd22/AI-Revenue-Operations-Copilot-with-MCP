# This repository handles dashboard-related database queries.

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.activity import Activity
from app.models.deal import Deal
from app.models.note import Note


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_accounts(self) -> int:
        return self.db.query(func.count(Account.id)).scalar() or 0

    def count_deals(self) -> int:
        return self.db.query(func.count(Deal.id)).scalar() or 0

    def count_activities(self) -> int:
        return self.db.query(func.count(Activity.id)).scalar() or 0

    def count_notes(self) -> int:
        return self.db.query(func.count(Note.id)).scalar() or 0

    def get_deals_grouped_by_risk(self) -> list[tuple[str | None, int]]:
        return (
            self.db.query(Deal.risk_level, func.count(Deal.id))
            .group_by(Deal.risk_level)
            .all()
        )

    def get_deals_grouped_by_status(self) -> list[tuple[str, int]]:
        return (
            self.db.query(Deal.status, func.count(Deal.id))
            .group_by(Deal.status)
            .all()
        )

    def get_recent_accounts(self, limit: int = 5) -> list[Account]:
        return self.db.query(Account).order_by(Account.id.desc()).limit(limit).all()

    def get_recent_deals(self, limit: int = 5) -> list[Deal]:
        return self.db.query(Deal).order_by(Deal.id.desc()).limit(limit).all()

    def get_recent_activities(self, limit: int = 5) -> list[Activity]:
        return self.db.query(Activity).order_by(Activity.id.desc()).limit(limit).all()

    def get_recent_notes(self, limit: int = 5) -> list[Note]:
        return self.db.query(Note).order_by(Note.id.desc()).limit(limit).all()