from enum import Enum


class MessageType(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class Role(str, Enum):
    USER = 'user'
    BOT = 'bot'
