from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.injector import container
from app.schema.user_schema import UserCreateRequest, UserResponse, ListUserResponse

user_router = APIRouter(tags=['User'])
user_service = container.user_service()
get_db = container.database().get_db


@user_router.post('/user')
async def create(req: UserCreateRequest, db: Session = Depends(get_db)) -> UserResponse:
    return await user_service.create(db, req)


@user_router.get('/user/{_id}')
async def find_by_id(_id: int, db: Session = Depends(get_db)) -> UserResponse:
    return await user_service.find_by_id(db, _id)


@user_router.get('/user')
async def search(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)) -> ListUserResponse:
    users, total = await user_service.search(db, page=page, page_size=page_size)
    return ListUserResponse(data=users, page=page, page_size=page_size, total=total)
