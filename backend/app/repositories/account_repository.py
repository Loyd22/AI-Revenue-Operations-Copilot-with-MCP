# This file handles database actions for accounts.
# It can:
# - get all accounts
# - get one account
# - create an account
# - save account updates
#
# It only talks to the database.
# It does not handle business rules.

from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:
    """
    Database helper for account records.
    """

    def __init__(self, db: Session):
        # Save the database connection/session
        self.db = db

    def get_all(self) -> list[Account]:
        # Return all accounts, newest first
        return self.db.query(Account).order_by(Account.id.desc()).all()

    def get_by_id(self, account_id: int) -> Account | None:
        # Find one account by its ID
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_name(self, name: str) -> Account | None:
        # Find one account by its name
        return self.db.query(Account).filter(Account.name == name).first()

    def create(self, account: Account) -> Account:
        # Save a new account to the database
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account: Account) -> Account:
        # Save changes to an existing account
        self.db.commit()
        self.db.refresh(account)
        return account