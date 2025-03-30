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
    OTHER = 'other'
