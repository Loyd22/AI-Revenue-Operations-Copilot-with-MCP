# This file handles the account business rules.
# It checks the rules first before saving or reading data from the database.
#
# Example:
# - if the account does not exist, return an error
# - if the account name already exists, do not allow duplicates

from sqlalchemy.orm import Session

from app.models.account import Account
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreateRequest, AccountUpdateRequest


class AccountService:
    """
    Business logic for account actions.
    """

    def __init__(self, db: Session):
        # Use the account repository for database work
        self.account_repository = AccountRepository(db)

    def list_accounts(self) -> list[Account]:
        # Return all accounts
        return self.account_repository.get_all()

    def get_account(self, account_id: int) -> Account:
        # Find one account by ID
        # If not found, raise an error
        account = self.account_repository.get_by_id(account_id)
        if account is None:
            raise ValueError("Account not found.")
        return account

    def create_account(self, payload: AccountCreateRequest) -> Account:
        # Check if an account with the same name already exists
        existing_account = self.account_repository.get_by_name(payload.name)
        if existing_account is not None:
            raise ValueError("An account with this name already exists.")

        # Create a new Account object from the request data
        account = Account(
            name=payload.name,
            industry=payload.industry,
            company_size=payload.company_size,
            status=payload.status,
            health_status=payload.health_status,
            renewal_date=payload.renewal_date,
            owner_user_id=payload.owner_user_id,
        )

        # Save the new account using the repository
        return self.account_repository.create(account)

    def update_account(self, account_id: int, payload: AccountUpdateRequest) -> Account:
        # Find the account first
        account = self.account_repository.get_by_id(account_id)
        if account is None:
            raise ValueError("Account not found.")

        # Get only the fields that were actually sent in the update request
        update_data = payload.model_dump(exclude_unset=True)

        # If the name is changing, make sure the new name is still unique
        if "name" in update_data and update_data["name"] != account.name:
            existing_account = self.account_repository.get_by_name(update_data["name"])
            if existing_account is not None:
                raise ValueError("An account with this name already exists.")

        # Apply each updated field to the account object
        for field, value in update_data.items():
            setattr(account, field, value)

        # Save the updated account
        return self.account_repository.update(account)