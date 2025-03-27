from pydantic import BaseModel, ConfigDict


class ConversationCreateRequest(BaseModel):
    user_id: int
    title: str


class ConversationResponse(ConversationCreateRequest):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ListConversationResponse(BaseModel):
    data: list[ConversationResponse]
    page: int
    page_size: int
    total: int
