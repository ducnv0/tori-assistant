from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.constant import MessageType, Role
from app.exception import ValidationError
from app.model.base import Base
from app.util.validation_util import validate_enum


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversation.id'))
    role: Mapped[Role] = mapped_column(String)
    message_type: Mapped[MessageType] = mapped_column(String)
    content: Mapped[str | None] = mapped_column(Text)
    file_path: Mapped[str | None] = mapped_column(Text)

    def validate(self):
        """Validates message fields before saving to the database."""
        self.role = validate_enum(self.role, enum=Role, field_name='role')
        self.message_type = validate_enum(
            self.message_type, enum=MessageType, field_name='message_type'
        )
        if self.message_type == MessageType.TEXT:
            if not self.content:
                raise ValidationError('content is required for text message')
            self.file_path = None
        elif not self.file_path:
            raise ValidationError('file_path is required for image/audio/video message')

        # TODO: more validation
