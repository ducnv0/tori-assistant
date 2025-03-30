from enum import Enum


class MessageType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class Role(str, Enum):
    USER = 'user'
    BOT = 'bot'


class WSReceiveType(str, Enum):
    RECEIVE = 'websocket.receive'
    DISCONNECT = 'websocket.disconnect'
    OTHER = 'other'


class WSDataType(str, Enum):
    TEXT_MESSAGE = 'text_message'
    AUDIO_MESSAGE = 'audio_message'
    IMAGE_MESSAGE = 'image_message'
    VIDEO_MESSAGE = 'video_message'
    TIMEZONE = 'timezone'
    ERROR = 'error'
    OTHER = 'other'

    def to_MESSAGE_TYPE(self):
        if self == WSDataType.TEXT_MESSAGE:
            return MessageType.TEXT
        elif self == WSDataType.AUDIO_MESSAGE:
            return MessageType.AUDIO
        elif self == WSDataType.IMAGE_MESSAGE:
            return MessageType.IMAGE
        elif self == WSDataType.VIDEO_MESSAGE:
            return MessageType.VIDEO
        else:
            raise ValueError(f'Invalid MessageType: {self}')

    @staticmethod
    def from_MESSAGE_TYPE(message_type: MessageType):
        if message_type == MessageType.TEXT:
            return WSDataType.TEXT_MESSAGE
        elif message_type == MessageType.AUDIO:
            return WSDataType.AUDIO_MESSAGE
        elif message_type == MessageType.IMAGE:
            return WSDataType.IMAGE_MESSAGE
        elif message_type == MessageType.VIDEO:
            return WSDataType.VIDEO_MESSAGE
        else:
            raise ValueError(f'Invalid MessageType: {message_type}')


class WSResponseType(str, Enum):
    ERROR = 'error'
    MESSAGE = 'message'
