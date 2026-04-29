# This repository handles database operations for notes.

from sqlalchemy.orm import Session

from app.models.note import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Note]:
        return self.db.query(Note).order_by(Note.id.desc()).all()

    def get_by_id(self, note_id: int) -> Note | None:
        return self.db.query(Note).filter(Note.id == note_id).first()

    def create(self, note: Note) -> Note:
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: Note) -> Note:
        self.db.commit()
        self.db.refresh(note)
        return note