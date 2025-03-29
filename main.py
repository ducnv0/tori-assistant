import logging

import uvicorn
from fastapi import FastAPI

from app.api.chat_api import chat_router
from app.api.conversation_api import conversation_router
from app.api.message_api import message_router
from app.api.user_api import user_router
from config import Config

# Configuration settings
logging.basicConfig(level=Config.LOGGING_LEVEL)

app = FastAPI()

app.include_router(user_router, prefix='/api')
app.include_router(conversation_router, prefix='/api')
app.include_router(message_router, prefix='/api')
app.include_router(chat_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False)
