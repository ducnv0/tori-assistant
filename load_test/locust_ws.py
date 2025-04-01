import json
import random
import threading
import time
import uuid
from sys import maxsize

import requests
import websocket
from locust import between, events, task
from locust_plugins.users.socketio import SocketIOUser

HOST_HTTP = 'http://localhost:8000'
HOST_WS = 'ws://localhost:8000'
RUNNING_USER_IDS = []
AUDIO_PATH = 'static/example_audio.mp3'
VIDEO_PATH = 'static/example_video.mp4'
with open(AUDIO_PATH, 'rb') as f:
    AUDIO_MESSAGE = f.read()

with open(VIDEO_PATH, 'rb') as f:
    VIDEO_MESSAGE = f.read()


class MySocketIOUser(SocketIOUser):
    wait_time = between(1, 3)  # Simulates users waiting between requests

    _lock = threading.Lock()

    def get_user_id(self) -> int:
        with self._lock:
            res = requests.get(
                f'{HOST_HTTP}/api/user', params={'page': 1, 'page_size': maxsize}
            )
            assert res.status_code == 200, res.text
            users = res.json()['data']
            user_ids = [user['id'] for user in users]
            for user_id in user_ids:
                if user_id not in RUNNING_USER_IDS:
                    RUNNING_USER_IDS.append(user_id)
                    return user_id

            # create new user if all users are running
            res = requests.post(
                f'{HOST_HTTP}/api/user', json={'username': f'User {uuid.uuid4()}'}
            )
            assert res.status_code == 200, res.text
            user_id = res.json()['id']
            RUNNING_USER_IDS.append(user_id)
            return user_id

    def get_conversation_id(self) -> int:
        user_id = self.get_user_id()
        res = requests.get(
            f'{HOST_HTTP}/api/conversation',
            params={'user_id': user_id, 'page': 1, 'page_size': 10},
        )
        assert res.status_code == 200, res.text
        conversations = res.json()['data']
        if len(conversations) > 0:
            return conversations[0]['id']

        # create new conversation if no conversation found
        res = requests.post(
            f'{HOST_HTTP}/api/conversation',
            json={'user_id': user_id, 'title': f'Conversation {uuid.uuid4()}'},
        )
        assert res.status_code == 200, res.text
        conversation = res.json()
        return conversation['id']

    def on_start(self):
        self.connect(
            f'ws://localhost:8000/api/chat?conversation_id={self.get_conversation_id()}'
        )
        self.send_timezone()

    def send_timezone(self):
        timezone_message = json.dumps({'timezone': 'Asia/Saigon'})
        self.send(timezone_message, name='timezone')

    def send_text(self, text: str):
        text_message = json.dumps({'text': text})
        self.send(text_message, name='text')

    def send_audio(self):
        self.send(AUDIO_MESSAGE, name='audio', opcode=websocket.ABNF.OPCODE_BINARY)

    def send_video(self):
        self.send(VIDEO_MESSAGE, name='video', opcode=websocket.ABNF.OPCODE_BINARY)

    @task
    def my_task(self):
        start_time = time.time()
        self.response = None

        message_type = random.choice(['text', 'audio', 'video'])
        if message_type == 'text':
            text_message = f'Hello time: {time.time()}'
            self.send_text(text_message)
        elif message_type == 'audio':
            self.send_audio()
        elif message_type == 'video':
            self.send_video()

        while not self.response:
            time.sleep(0.1)

        response_time = int((time.time() - start_time) * 1000)
        events.request.fire(
            request_type='WSS',
            name=message_type,
            response_time=response_time,
            response_length=len(self.response),
        )

    def on_message(self, message):
        # print(message)
        self.response = json.loads(message).get('content', None)
