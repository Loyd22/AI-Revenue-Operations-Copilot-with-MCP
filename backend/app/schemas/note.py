# These schemas define the input and output shapes for notes.

from pydantic import BaseModel


class NoteBase(BaseModel):
    account_id: int
    deal_id: int | None = None
    user_id: int | None = None
    note_type: str
    content: str
    source: str = "manual"


class NoteCreateRequest(NoteBase):
    pass


class NoteUpdateRequest(BaseModel):
    account_id: int | None = None
    deal_id: int | None = None
    user_id: int | None = None
    note_type: str | None = None
    content: str | None = None
    source: str | None = None


class NoteResponse(BaseModel):
    id: int
    account_id: int
    deal_id: int | None
    user_id: int | None
    note_type: str
    content: str
    source: str

    model_config = {"from_attributes": True}