# This file contains the API routes for notes.
# In simple words, this is where the frontend can ask the backend to:
# - show all notes
# - show one note
# - create a new note
# - update an existing note

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# This checks that the user is logged in and active.
from app.core.dependencies import require_active_user

# This gives us a database session/connection.
from app.db.session import get_db

# This is the User model, used for the logged-in user.
from app.models.user import User

# These define the input and output format for notes.
from app.schemas.note import NoteCreateRequest, NoteResponse, NoteUpdateRequest

# This contains the note business logic.
from app.services.note_service import NoteService

# All routes in this file will start with /notes
# Example:
# - GET /notes
# - POST /notes
router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("")
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return all notes.

    In simple words:
    this route gives the logged-in user the full list of note records.
    """
    # Create the service so we can use the note logic.
    note_service = NoteService(db)

    # Ask the service to get all notes.
    notes = note_service.list_notes()

    # Return the notes in a clean response format.
    return {
        "success": True,
        "message": "Notes fetched successfully",
        "data": [NoteResponse.model_validate(note).model_dump() for note in notes],
    }


@router.get("/{note_id}")
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return one note by ID.

    In simple words:
    this route gives the details of one specific note record.
    """
    # Create the service for note logic.
    note_service = NoteService(db)

    try:
        # Ask the service to find the note by ID.
        note = note_service.get_note(note_id)

        # If found, return it in a clean response format.
        return {
            "success": True,
            "message": "Note fetched successfully",
            "data": NoteResponse.model_validate(note).model_dump(),
        }
    except ValueError as exc:
        # If the note does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("")
def create_note(
    payload: NoteCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Create a new note.

    In simple words:
    this route adds a new note record to the CRM.
    """
    # Create the service for note logic.
    note_service = NoteService(db)

    # Ask the service to create the note using the request data.
    note = note_service.create_note(payload)

    # Return the newly created note.
    return {
        "success": True,
        "message": "Note created successfully",
        "data": NoteResponse.model_validate(note).model_dump(),
    }


@router.patch("/{note_id}")
def update_note(
    note_id: int,
    payload: NoteUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Update a note.

    In simple words:
    this route changes some details of an existing note record.
    """
    # Create the service for note logic.
    note_service = NoteService(db)

    try:
        # Ask the service to update the note with the new data.
        note = note_service.update_note(note_id, payload)

        # Return the updated note.
        return {
            "success": True,
            "message": "Note updated successfully",
            "data": NoteResponse.model_validate(note).model_dump(),
        }
    except ValueError as exc:
        # If the note does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc