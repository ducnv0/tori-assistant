from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.exception import ValidationError
from app.model.base import Base


class Conversation(Base):
    __tablename__ = 'conversation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    title: Mapped[str] = mapped_column(String, default='New Conversation')

    def validate(self):
        if not self.title or len(self.title) > 100:
            raise ValidationError('title must be between 1 and 100 characters')
        # TODO: more validation
