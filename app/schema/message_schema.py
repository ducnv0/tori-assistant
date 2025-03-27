from pydantic import BaseModel, ConfigDict
from app.constant import MessageType, Role


class MessageCreateRequest(BaseModel):
    conversation_id: int
    role: Role
    message_type: MessageType
    content: str | None = None
    file_path: str | None = None


class MessageResponse(MessageCreateRequest):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ListMessageResponse(BaseModel):
    data: list[MessageResponse]
    page: int
    page_size: int
    total: int
