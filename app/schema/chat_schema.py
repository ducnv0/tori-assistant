import json

from pydantic import BaseModel, model_validator

from app.constant import WSDataType, WSReceiveType
from app.util.common_util import check_file_type


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
    mine_type: str | None = None
    text_message: str | None = None
    timezone: str | None = None
    image_message: bytes | None = None
    audio_message: bytes | None = None
    video_message: bytes | None = None
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
            file_type, mine = check_file_type(bytes)
            new_values['mine_type'] = mine
            if file_type == WSDataType.AUDIO_MESSAGE:
                new_values['audio_message'] = bytes
            elif file_type == WSDataType.VIDEO_MESSAGE:
                new_values['video_message'] = bytes
            elif file_type == WSDataType.IMAGE_MESSAGE:
                new_values['image_message'] = bytes

        new_values['raw_data'] = values
        return new_values

    @model_validator(mode='after')
    def fill_data(self):
        if self.type == WSReceiveType.RECEIVE:
            if self.text_message:
                self.data_type = WSDataType.TEXT_MESSAGE
            elif self.audio_message:
                self.data_type = WSDataType.AUDIO_MESSAGE
            elif self.video_message:
                self.data_type = WSDataType.VIDEO_MESSAGE
            elif self.image_message:
                self.data_type = WSDataType.IMAGE_MESSAGE
            elif self.timezone:
                self.data_type = WSDataType.TIMEZONE
            else:
                self.data_type = WSDataType.OTHER
        return self

    @property
    def need_to_process(self):
        return self.type == WSReceiveType.RECEIVE and self.data_type in [
            WSDataType.TEXT_MESSAGE,
            WSDataType.AUDIO_MESSAGE,
            WSDataType.VIDEO_MESSAGE,
            WSDataType.IMAGE_MESSAGE,
        ]
