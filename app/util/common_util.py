import filetype
from filetype.types import AUDIO, IMAGE, VIDEO

from app.constant import WSDataType
from app.exception import ValidationError


def get_offset_limit(page: int, page_size: int) -> (int, int):
    """
    page start from 1, page_size is the number of items per page
    """
    if page < 1:
        raise ValidationError('Page must be greater than 0')
    if page_size < 1:
        raise ValidationError('Page size must be greater than 0')
    offset = (page - 1) * page_size
    limit = page_size
    return offset, limit


AUDIO_EXTENSIONS = {it.EXTENSION for it in AUDIO}
VIDEO_EXTENSIONS = {it.EXTENSION for it in VIDEO}
IMAGE_EXTENSIONS = {it.EXTENSION for it in IMAGE}


def check_file_type(filelike: str | bytes) -> (WSDataType, str):
    kind = filetype.guess(filelike)
    mine = None
    if kind:
        mine = kind.mime
        if kind.extension in AUDIO_EXTENSIONS:
            return WSDataType.AUDIO_MESSAGE, mine
        elif kind.extension in VIDEO_EXTENSIONS:
            return WSDataType.VIDEO_MESSAGE, mine
        elif kind.extension in IMAGE_EXTENSIONS:
            return WSDataType.IMAGE_MESSAGE, mine
    return WSDataType.OTHER, mine
