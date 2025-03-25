from enum import Enum


class MessageTypeEnum(str, Enum):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    FILE = 'file'

class MessageStatusEnum(str, Enum):
    PENDING = 'pending'
    SENT = 'sent'
    FAILED = 'failed'
    RECEIVED = 'received'