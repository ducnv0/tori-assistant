import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import MessageType, Role
from app.exception import NotFoundError
from app.model.message import Message
from app.repository.message_repository import MessageRepository
from app.schema.message_schema import MessageCreateRequest, MessageResponse
from app.service.conversation_service import ConversationService
from app.service.storage_service import StorageService


class MessageService:
    def __init__(
        self,
        message_repository: MessageRepository,
        conversation_service: ConversationService,
        storage_service: StorageService,
    ):
        self.message_repository = message_repository
        self.conversation_service = conversation_service
        self.storage_service = storage_service

    async def find_by_id(self, db: AsyncSession, _id: int) -> Message:
        message = await self.message_repository.find_by_id(db, _id)
        if not message:
            raise NotFoundError(f'Message with id {_id} not found')
        return message

    async def read_message(
        self, db: AsyncSession, message: Message | None = None, _id: int | None = None
    ) -> MessageResponse:
        if not _id and not message:
            raise ValueError('Either _id or message must be provided')
        if _id:
            message = await self.find_by_id(db, _id)
        message_response = MessageResponse.model_validate(message)
        if message_response.file_path and not message_response.file_path.startswith(
            'http'
        ):
            message_response.file_path = (
                await self.storage_service.get_public_url_async(message.file_path)
            )
        return message_response

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

    async def create_text_message(
        self,
        db: AsyncSession,
        conversation_id: int,
        role: Role,
        content: str,
    ) -> Message:
        req = MessageCreateRequest(
            conversation_id=conversation_id,
            role=role,
            message_type=MessageType.TEXT,
            content=content,
        )
        return await self.create(db, req)

    async def create_file_message(
        self,
        db: AsyncSession,
        conversation_id: int,
        role: Role,
        data: bytes,
        message_type: MessageType,
        content_type: str | None = None,
    ) -> Message:
        file_path = self.gen_file_path(
            conversation_id=conversation_id, role=role, message_type=message_type
        )
        req = MessageCreateRequest(
            conversation_id=conversation_id,
            role=role,
            message_type=message_type,
            file_path=file_path,
        )
        await self.storage_service.upload_binary_async(
            data=data,
            object_name=file_path,
            content_type=content_type,
        )
        return await self.create(db, req)

    def gen_file_path(
        self, conversation_id: int, role: Role, message_type: MessageType
    ) -> str:
        return f'{conversation_id}/{role}/{message_type}/{uuid.uuid4()}'
