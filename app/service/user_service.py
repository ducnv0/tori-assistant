from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import NotFoundError
from app.model import User
from app.repository.user_repository import UserRepository
from app.schema.user_schema import UserCreateRequest


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def find_by_id(self, db: AsyncSession, _id: int) -> User:
        user = await self.user_repository.find_by_id(db, _id)
        if not user:
            raise NotFoundError(f'User with id {_id} not found')
        return user

    async def create(self, db: AsyncSession, req: UserCreateRequest) -> User:
        user = User(username=req.username)
        user.validate()
        return await self.user_repository.create(db, user)

    async def search(
        self, db: AsyncSession, page: int, page_size: int
    ) -> (list[User], int):
        return await self.user_repository.search(db, page=page, page_size=page_size)
