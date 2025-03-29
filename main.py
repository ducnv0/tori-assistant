import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.chat_api import chat_router
from app.api.conversation_api import conversation_router
from app.api.fe_api import fe_router
from app.api.message_api import message_router
from app.api.user_api import user_router
from config import Config

# Configuration settings
logging.basicConfig(level=Config.LOGGING_LEVEL)


# Apply the filter to the aiosqlite logger
aiosqlite_logger = logging.getLogger('aiosqlite').setLevel(logging.INFO)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

# Add CORS middleware
# Just for testing purpose, allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Allow all origins
    allow_credentials=True,
    allow_methods=['*'],  # Allow all methods
    allow_headers=['*'],  # Allow all headers
)

app.include_router(user_router, prefix='/api')
app.include_router(conversation_router, prefix='/api')
app.include_router(message_router, prefix='/api')
app.include_router(chat_router, prefix='/api')
app.include_router(fe_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=False)
