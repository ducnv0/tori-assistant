# Configuration settings
import logging

from config import Config

logging.basicConfig(level=Config.LOGGING_LEVEL)
# Apply the filter to the aiosqlite logger
aiosqlite_logger = logging.getLogger('aiosqlite').setLevel(logging.INFO)
urllib3_logger = logging.getLogger('urllib3').setLevel(logging.INFO)


import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.chat_api import chat_router
from app.api.conversation_api import conversation_router
from app.api.fe_api import fe_router
from app.api.message_api import message_router
from app.api.user_api import user_router
from app.injector import container


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with container.database().AsyncSessionLocal() as db:
        # FIXME: Should out source this task to celery
        task = asyncio.create_task(
            container.websocket_connection_service().periodically_clean_stale_connections(
                db
            )
        )

        yield  # Startup event

        task.cancel()  # Shutdown event


app = FastAPI(lifespan=lifespan)
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
