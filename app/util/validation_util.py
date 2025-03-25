from enum import Enum

from app.exception import ValidationError

def validate_enum(value: str, enum: Enum | list[str], field_name: str) -> str:
    """Validates if a value is within a list of allowed enum values."""
    if isinstance(enum, Enum):
        enum = list(enum)
    if value not in enum:
        raise ValidationError(f'Invalid {field_name}: {value}. Must be one of {enum}')
    return value
