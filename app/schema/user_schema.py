from pydantic import BaseModel, ConfigDict


class UserCreateRequest(BaseModel):
    username: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class ListUserResponse(BaseModel):
    data: list[UserResponse]
    page: int
    page_size: int
    total: int