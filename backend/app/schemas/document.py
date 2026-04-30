# These schemas define the input and output shapes for documents.

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    title: str
    file_name: str
    storage_path: str
    document_type: str
    status: str
    uploaded_by_user_id: int | None

    model_config = {"from_attributes": True}