from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.message import Message
from app.util.common_util import get_offset_limit


class MessageRepository:
    async def find_by_id(self, db: AsyncSession, _id: int) -> Message | None:
        return await db.get(Message, _id)

    async def create(self, db: AsyncSession, message: Message) -> Message:
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message


    async def search(self, db: AsyncSession, conversation_id: int, page: int, page_size: int,) -> (list[Message], int):
        offset, limit = get_offset_limit(page, page_size)
        filters = [Message.conversation_id == conversation_id]

        stmt = select(Message).where(*filters).order_by(Message.id.desc())  # FIXME: should be ordered by created_at
        results = await db.execute(stmt.offset(offset).limit(limit))
        messages = results.scalars().all()

        total_stmt = select(func.count()).select_from(Message).where(*filters)
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar()

        return messages, total_count
