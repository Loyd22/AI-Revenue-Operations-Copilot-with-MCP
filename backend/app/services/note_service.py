# This file handles the business rules for notes.
# In simple words, it decides:
# - how to get notes
# - what to do if a note is missing
# - how to create a new note
# - how to update a note
#
# It does not directly do raw database queries.
# That part is handled by the repository.

from sqlalchemy.orm import Session

from app.models.note import Note
from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreateRequest, NoteUpdateRequest


class NoteService:
    """
    Business logic for note actions.
    """

    def __init__(self, db: Session):
        # Use the note repository for database work
        self.note_repository = NoteRepository(db)

    def list_notes(self) -> list[Note]:
        # Return all notes
        return self.note_repository.get_all()

    def get_note(self, note_id: int) -> Note:
        # Find one note by ID
        # If it does not exist, return an error
        note = self.note_repository.get_by_id(note_id)
        if note is None:
            raise ValueError("Note not found.")
        return note

    def create_note(self, payload: NoteCreateRequest) -> Note:
        # Create a new Note object from the request data
        note = Note(
            account_id=payload.account_id,
            deal_id=payload.deal_id,
            user_id=payload.user_id,
            note_type=payload.note_type,
            content=payload.content,
            source=payload.source,
        )

        # Save the new note using the repository
        return self.note_repository.create(note)

    def update_note(self, note_id: int, payload: NoteUpdateRequest) -> Note:
        # Find the note first
        note = self.note_repository.get_by_id(note_id)
        if note is None:
            raise ValueError("Note not found.")

        # Get only the fields that were actually sent in the update request
        update_data = payload.model_dump(exclude_unset=True)

        # Apply each updated field to the note object
        for field, value in update_data.items():
            setattr(note, field, value)

        # Save the updated note
        return self.note_repository.update(note)