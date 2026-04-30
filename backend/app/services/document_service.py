# This file handles the business rules for documents.
# In simple words, it decides:
# - how to get documents
# - what to do if a document is missing
# - how to save an uploaded file
# - how to create the document record in the database
#
# It uses the repository for database work.

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    """
    Business logic for document actions.
    """

    def __init__(self, db: Session):
        # Use the document repository for database work
        self.document_repository = DocumentRepository(db)

    def list_documents(self) -> list[Document]:
        # Return all documents
        return self.document_repository.get_all()

    def get_document(self, document_id: int) -> Document:
        # Find one document by ID
        # If it does not exist, return an error
        document = self.document_repository.get_by_id(document_id)
        if document is None:
            raise ValueError("Document not found.")
        return document

    def create_document(
        self,
        title: str,
        document_type: str,
        file: UploadFile,
        uploaded_by_user_id: int | None,
    ) -> Document:
        # Check if another document already has the same title
        existing_document = self.document_repository.get_by_title(title)
        if existing_document is not None:
            raise ValueError("A document with this title already exists.")

        # Get the main storage folder from project settings
        storage_root = Path(settings.local_storage_path)

        # Create a "documents" folder inside the storage folder if it does not exist yet
        documents_dir = storage_root / "documents"
        documents_dir.mkdir(parents=True, exist_ok=True)

        # Get the original file extension, like .pdf or .docx
        file_extension = Path(file.filename or "").suffix

        # Create a safe unique filename so uploaded files do not overwrite each other
        safe_filename = f"{uuid4()}{file_extension}"

        # Build the full file path where the uploaded file will be saved
        file_path = documents_dir / safe_filename

        # Read the uploaded file content
        file_bytes = file.file.read()

        # Save the uploaded file to the local storage folder
        file_path.write_bytes(file_bytes)

        # Create the document record that will be saved in the database
        document = Document(
            title=title,
            file_name=file.filename or safe_filename,
            storage_path=str(file_path).replace("\\", "/"),
            document_type=document_type,
            status="uploaded",
            uploaded_by_user_id=uploaded_by_user_id,
        )

        # Save the document record using the repository
        return self.document_repository.create(document)