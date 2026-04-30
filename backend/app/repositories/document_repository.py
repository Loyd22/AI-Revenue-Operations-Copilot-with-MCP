# This file handles database actions for documents.
# In simple words, it can:
# - get all documents
# - get one document
# - find a document by title
# - save a new document
#
# It only talks to the database.
# It does not handle business rules.

from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    """
    Database helper for document records.
    """

    def __init__(self, db: Session):
        # Save the database connection/session
        self.db = db

    def get_all(self) -> list[Document]:
        # Return all documents, newest first
        return self.db.query(Document).order_by(Document.id.desc()).all()

    def get_by_id(self, document_id: int) -> Document | None:
        # Find one document by its ID
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_by_title(self, title: str) -> Document | None:
        # Find one document by its title
        return self.db.query(Document).filter(Document.title == title).first()

    def create(self, document: Document) -> Document:
        # Save a new document to the database
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document