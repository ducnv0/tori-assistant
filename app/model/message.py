from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.constant import MessageTypeEnum
from app.model.base import Base
from app.util.validation_util import validate_enum


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversation.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    message_type: Mapped[str] = mapped_column(String)
    content: Mapped[str | None] = mapped_column(Text)
    file_path: Mapped[str | None] = mapped_column(Text)

    def validate(self):
        """Validates message fields before saving to the database."""
        self.message_type = validate_enum(self.message_type, enum=MessageTypeEnum, field_name='message_type')
        # TODO: more validation

