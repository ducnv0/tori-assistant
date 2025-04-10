from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.injector import container
from app.schema.message_schema import ListMessageResponse, MessageResponse

message_router = APIRouter(tags=['Message'])
message_service = container.message_service()
get_db = container.database().get_db


@message_router.get('/message/{_id}')
async def find_by_id(_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    message = await message_service.find_by_id(db, _id)
    return await message_service.read_message(db, message)


@message_router.get('/message')
async def search(
    conversation_id: int,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
) -> ListMessageResponse:
    messages, total = await message_service.search(
        db, conversation_id=conversation_id, page=page, page_size=page_size
    )
    return ListMessageResponse(
        data=[await message_service.read_message(db, message) for message in messages],
        page=page,
        page_size=page_size,
        total=total,
    )
