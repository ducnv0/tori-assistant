from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.model.message import Message
from app.repository.message_repository import MessageRepository
from app.schema.message_schema import MessageCreateRequest
from app.service.conversation_service import ConversationService


class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_service: ConversationService,
    ):
        self.message_repository = message_repository
        self.conversation_service = conversation_service

    async def find_by_id(self, db: AsyncSession, _id: int) -> Message:
        message = await self.message_repository.find_by_id(db, _id)
        if not message:
            raise NotFoundError(f'Message with id {_id} not found')
        return message

    async def create(self, db: AsyncSession, req: MessageCreateRequest) -> Message:
        await self.conversation_service.find_by_id(db, req.conversation_id)
        message = Message(
            conversation_id=req.conversation_id,
            role=req.role,
            message_type=req.message_type,
            content=req.content,
            file_path=req.file_path,
        )
        message.validate()
        return await self.message_repository.create(db, message)

    async def search(
        self, db: AsyncSession, conversation_id: int, page: int, page_size: int
    ) -> (list[Message], int):
        return await self.message_repository.search(
            db, conversation_id=conversation_id, page=page, page_size=page_size
        )
