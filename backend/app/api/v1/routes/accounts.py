# This file contains the API routes for accounts.
# In simple words, this is where the frontend can ask the backend to:
# - show all accounts
# - show one account
# - create a new account
# - update an existing account

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# This checks that the user is logged in and active.
from app.core.dependencies import require_active_user

# This gives us a database session/connection.
from app.db.session import get_db

# This is the User model, used for the logged-in user.
from app.models.user import User

# These define the input and output format for accounts.
from app.schemas.account import AccountCreateRequest, AccountResponse, AccountUpdateRequest

# This contains the account business logic.
from app.services.account_service import AccountService

# All routes in this file will start with /accounts
# Example:
# - GET /accounts
# - POST /accounts
router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("")
def list_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return all accounts.

    In simple words:
    this route gives the logged-in user the full list of customer companies.
    """
    # Create the service so we can use the account logic.
    account_service = AccountService(db)

    # Ask the service to get all accounts.
    accounts = account_service.list_accounts()

    # Return the accounts in a clean response format.
    return {
        "success": True,
        "message": "Accounts fetched successfully",
        "data": [AccountResponse.model_validate(account).model_dump() for account in accounts],
    }


@router.get("/{account_id}")
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return one account by ID.

    In simple words:
    this route gives the details of one specific customer company.
    """
    # Create the service for account logic.
    account_service = AccountService(db)

    try:
        # Ask the service to find the account by ID.
        account = account_service.get_account(account_id)

        # If found, return it in a clean response format.
        return {
            "success": True,
            "message": "Account fetched successfully",
            "data": AccountResponse.model_validate(account).model_dump(),
        }
    except ValueError as exc:
        # If the account does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("")
def create_account(
    payload: AccountCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Create a new account.

    In simple words:
    this route adds a new customer company to the CRM.
    """
    # Create the service for account logic.
    account_service = AccountService(db)

    try:
        # Ask the service to create the account using the request data.
        account = account_service.create_account(payload)

        # Return the newly created account.
        return {
            "success": True,
            "message": "Account created successfully",
            "data": AccountResponse.model_validate(account).model_dump(),
        }
    except ValueError as exc:
        # If something is wrong, like duplicate account name,
        # return a 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch("/{account_id}")
def update_account(
    account_id: int,
    payload: AccountUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Update an account.

    In simple words:
    this route changes some details of an existing customer company.
    """
    # Create the service for account logic.
    account_service = AccountService(db)

    try:
        # Ask the service to update the account with the new data.
        account = account_service.update_account(account_id, payload)

        # Return the updated account.
        return {
            "success": True,
            "message": "Account updated successfully",
            "data": AccountResponse.model_validate(account).model_dump(),
        }
    except ValueError as exc:
        # Decide which error code to return:
        # - 404 if the account does not exist
        # - 400 for other problems like duplicate account name
        message = str(exc)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if message == "Account not found."
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=status_code,
            detail=message,
        ) from exc