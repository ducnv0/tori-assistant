from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.model.base import Base
from app.exception import ValidationError

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)

    def validate(self):
        if not self.username or len(self.username) < 3:
            raise ValidationError('Username must be at least 3 characters long')
        # TODO: more validation