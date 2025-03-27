from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.model import User
from app.util.common_util import get_offset_limit


class UserRepository:
    async def find_by_id(self, db: AsyncSession, _id: int) -> User | None:
        return await db.get(User, _id)

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def search(self, db: AsyncSession, page: int, page_size: int) -> (list[User], int):
        offset, limit = get_offset_limit(page, page_size)
        stmt = select(User).order_by(User.id.desc())  # FIXME: should be ordered by created_at
        results = await db.execute(stmt.offset(offset).limit(limit))
        users = results.scalars().all()

        total_stmt = select(func.count()).select_from(User)
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar()

        return users, total_count
