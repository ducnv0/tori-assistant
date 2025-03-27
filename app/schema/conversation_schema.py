from pydantic import BaseModel, ConfigDict


class ConversationCreateRequest(BaseModel):
    user_id: int
    title: str


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str


class ListConversationResponse(BaseModel):
    data: list[ConversationResponse]
    page: int
    page_size: int
    total: int