# This file contains the API routes for documents.
# In simple words, this is where the frontend can ask the backend to:
# - show all documents
# - show one document
# - upload a new document

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

# This checks that the user is logged in and active.
from app.core.dependencies import require_active_user

# This gives us a database session/connection.
from app.db.session import get_db

# This is the User model, used for the logged-in user.
from app.models.user import User

# This defines the output format for documents.
from app.schemas.document import DocumentResponse

# This contains the document business logic.
from app.services.document_service import DocumentService

# All routes in this file will start with /documents
# Example:
# - GET /documents
# - POST /documents
router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("")
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return all documents.

    In simple words:
    this route gives the logged-in user the full list of uploaded documents.
    """
    # Create the service so we can use the document logic.
    document_service = DocumentService(db)

    # Ask the service to get all documents.
    documents = document_service.list_documents()

    # Return the documents in a clean response format.
    return {
        "success": True,
        "message": "Documents fetched successfully",
        "data": [
            DocumentResponse.model_validate(document).model_dump()
            for document in documents
        ],
    }


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return one document by ID.

    In simple words:
    this route gives the details of one specific document record.
    """
    # Create the service for document logic.
    document_service = DocumentService(db)

    try:
        # Ask the service to find the document by ID.
        document = document_service.get_document(document_id)

        # If found, return it in a clean response format.
        return {
            "success": True,
            "message": "Document fetched successfully",
            "data": DocumentResponse.model_validate(document).model_dump(),
        }
    except ValueError as exc:
        # If the document does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("")
def create_document(
    title: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Upload a new document.

    In simple words:
    this route receives a file and its details,
    saves the file, and creates a document record in the database.
    """
    # Create the service for document logic.
    document_service = DocumentService(db)

    try:
        # Ask the service to save the uploaded file and create the document record.
        document = document_service.create_document(
            title=title,
            document_type=document_type,
            file=file,
            uploaded_by_user_id=current_user.id,
        )

        # Return the newly created document.
        return {
            "success": True,
            "message": "Document uploaded successfully",
            "data": DocumentResponse.model_validate(document).model_dump(),
        }
    except ValueError as exc:
        # If something is wrong, like duplicate document title,
        # return a 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc