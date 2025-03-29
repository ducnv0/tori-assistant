from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import Conversation
from app.util.common_util import get_offset_limit


class ConversationRepository:
    async def find_by_id(self, db: AsyncSession, _id: int) -> Conversation | None:
        return await db.get(Conversation, _id)

    async def create(
        self,
        db: AsyncSession,
        conversation: Conversation,
    ) -> Conversation:
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        return conversation

    async def update(
        self,
        db: AsyncSession,
        conversation: Conversation,
    ) -> Conversation:
        await db.commit()
        await db.refresh(conversation)
        return conversation

    async def search(
        self,
        db: AsyncSession,
        user_id: int,
        page: int,
        page_size: int,
    ) -> (list[Conversation], int):
        offset, limit = get_offset_limit(page, page_size)
        filters = [Conversation.user_id == user_id]

        stmt = (
            select(Conversation).where(*filters).order_by(Conversation.id.desc())
        )  # FIXME: should be ordered by created_at
        results = await db.execute(stmt.offset(offset).limit(limit))
        conversations = results.scalars().all()

        total_stmt = select(func.count()).select_from(Conversation).where(*filters)
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar()

        return conversations, total_count
