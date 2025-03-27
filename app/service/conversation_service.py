from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.model import Conversation
from app.repository.conversation_repository import ConversationRepository
from app.schema.conversation_schema import ConversationCreateRequest
from app.service.user_service import UserService


class ConversationService:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        user_service: UserService,
    ):
        self.conversation_repository = conversation_repository
        self.user_service = user_service

    async def find_by_id(self, db: AsyncSession, _id: int) -> Conversation:
        conversation = await self.conversation_repository.find_by_id(db, _id)
        if not conversation:
            raise NotFoundError(f'Conversation with id {_id} not found')
        return conversation

    async def create(
        self,
        db: AsyncSession,
        req: ConversationCreateRequest,
    ) -> Conversation:
        await self.user_service.find_by_id(db, req.user_id)
        conversation = Conversation(user_id=req.user_id, title=req.title)
        conversation.validate()
        return await self.conversation_repository.create(db, conversation)

    async def search(
        self, db: AsyncSession, user_id: int, page: int, page_size: int
    ) -> (list[Conversation], int):
        return await self.conversation_repository.search(
            db, user_id=user_id, page=page, page_size=page_size
        )
