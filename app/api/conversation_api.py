from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.injector import container
from app.schema.conversation_schema import (
    ConversationCreateRequest,
    ConversationResponse,
    ListConversationResponse,
)

conversation_router = APIRouter(tags=['Conversation'])
conversation_service = container.conversation_service()
get_db = container.database().get_db


@conversation_router.post('/conversation')
async def create(
    req: ConversationCreateRequest,
    db: Session = Depends(get_db),
) -> ConversationResponse:
    return await conversation_service.create(db, req)


@conversation_router.get('/conversation/{_id}')
async def find_by_id(_id: int, db: Session = Depends(get_db)) -> ConversationResponse:
    return await conversation_service.find_by_id(db, _id)


@conversation_router.get('/conversation')
async def search(
    user_id: int, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)
) -> ListConversationResponse:
    conversations, total = await conversation_service.search(
        db,
        user_id=user_id,
        page=page,
        page_size=page_size,
    )
    return ListConversationResponse(
        data=conversations,
        page=page,
        page_size=page_size,
        total=total,
    )
