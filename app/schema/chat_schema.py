import json

from pydantic import BaseModel, model_validator

from app.constant import WSDataType, WSReceiveType


class ReceiveMessage(BaseModel):
    """
    Example:
    disconnect: {'code': <CloseCode.NO_STATUS_RCVD: 1005>, 'reason': '', 'type': 'websocket.disconnect'}
    bytes: {'bytes': b'\xff\...', 'type': 'websocket.receive'}
    text: {'text': '{"text": "Hello"}', 'type': 'websocket.receive'}
    timezone: {'text': '{"timezone": "Asia/Saigon"}', 'type': 'websocket.receive'}

    """

    type: WSReceiveType
    data_type: WSDataType | None = None
    text_message: str | None = None
    timezone: str | None = None
    bytes_message: bytes | None = None
    raw_data: dict | None = None

    @model_validator(mode='before')
    def prepare_data(cls, values):
        new_values = {}

        # type
        type = values.get('type', '')
        if type not in list(WSReceiveType):
            type = 'others'
        new_values['type'] = type

        text = values.get('text', None)
        if text:
            try:
                json_text = json.loads(text)
                text_message = json_text.get('text', None)
                timezone = json_text.get('timezone', None)
                if text_message:
                    new_values['text_message'] = text_message
                elif timezone:
                    new_values['timezone'] = timezone
            except json.JSONDecodeError:
                pass

        bytes = values.get('bytes', None)
        if bytes:
            new_values['bytes_message'] = bytes

        new_values['raw_data'] = values
        return new_values

    @model_validator(mode='after')
    def fill_data(self):
        if self.type == WSReceiveType.RECEIVE:
            if self.text_message:
                self.data_type = WSDataType.TEXT_MESSAGE
            elif self.bytes_message:
                self.data_type = WSDataType.BYTES_MESSAGE
            elif self.timezone:
                self.data_type = WSDataType.TIMEZONE
            else:
                self.data_type = WSDataType.OTHER
        return self
