import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.model.base import Base


class WebsocketConnection(Base):
    __tablename__ = 'websocket_connection'

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), primary_key=True
    )
    conversation_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('conversation.id'), primary_key=True
    )  # conversation id
    last_active: Mapped[datetime.datetime] = mapped_column(DateTime)

    def validate(self):
        # TODO: implement this
        pass
