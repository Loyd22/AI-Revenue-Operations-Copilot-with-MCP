# This file handles database actions for deals.
# In simple words, it can:
# - get all deals
# - get one deal
# - create a new deal
# - save updates to a deal
#
# It only talks to the database.
# It does not handle business rules.

from sqlalchemy.orm import Session

from app.models.deal import Deal


class DealRepository:
    """
    Database helper for deal records.
    """

    def __init__(self, db: Session):
        # Save the database connection/session
        self.db = db

    def get_all(self) -> list[Deal]:
        # Return all deals, newest first
        return self.db.query(Deal).order_by(Deal.id.desc()).all()

    def get_by_id(self, deal_id: int) -> Deal | None:
        # Find one deal by its ID
        return self.db.query(Deal).filter(Deal.id == deal_id).first()

    def get_by_title(self, title: str) -> Deal | None:
        # Find one deal by its title
        return self.db.query(Deal).filter(Deal.title == title).first()

    def create(self, deal: Deal) -> Deal:
        # Save a new deal to the database
        self.db.add(deal)
        self.db.commit()
        self.db.refresh(deal)
        return deal

    def update(self, deal: Deal) -> Deal:
        # Save changes to an existing deal
        self.db.commit()
        self.db.refresh(deal)
        return deal