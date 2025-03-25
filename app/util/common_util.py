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