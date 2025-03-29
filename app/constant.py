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
    BYTES_MESSAGE = 'bytes_message'
    TIMEZONE = 'timezone'
    OTHER = 'other'
