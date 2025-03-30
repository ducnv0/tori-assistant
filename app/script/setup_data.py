from app.injector import container
from app.model import Base
from app.schema.conversation_schema import ConversationCreateRequest
from app.schema.message_schema import MessageCreateRequest
from app.schema.user_schema import UserCreateRequest


async def setup_data():
    async with container.database().async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with container.database().AsyncSessionLocal() as db:
        # create users
        user_1 = await container.user_service().create(
            db=db,
            req=UserCreateRequest(username='user_1'),
        )
        user_2 = await container.user_service().create(
            db=db,
            req=UserCreateRequest(username='user_2'),
        )
        user_3 = await container.user_service().create(
            db=db,
            req=UserCreateRequest(username='user_3'),
        )

        # create conversations
        conversation_1 = await container.conversation_service().create(
            db=db,
            req=ConversationCreateRequest(user_id=user_1.id, title='conversation_1'),
        )
        conversation_2 = await container.conversation_service().create(
            db=db,
            req=ConversationCreateRequest(user_id=user_2.id, title='conversation_2'),
        )
        conversation_3 = await container.conversation_service().create(
            db=db,
            req=ConversationCreateRequest(user_id=user_3.id, title='conversation_3'),
        )
        conversation_4 = await container.conversation_service().create(
            db=db,
            req=ConversationCreateRequest(user_id=user_1.id, title='conversation_4'),
        )

        # message for conversation_1
        for message_data in [
            {
                'conversation_id': conversation_1.id,
                'role': 'user',
                'message_type': 'text',
                'content': 'Hello, how are you?',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'bot',
                'message_type': 'text',
                'content': 'I am fine, thank you.',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'user',
                'message_type': 'audio',
                'file_path': 'https://www.bensound.com/bensound-music/bensound-ukulele.mp3',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'bot',
                'message_type': 'text',
                'content': 'Your audio file has been received.',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'user',
                'message_type': 'image',
                'file_path': 'https://picsum.photos/seed/picsum/200/300',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'bot',
                'message_type': 'text',
                'content': 'Your image file has been received.',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'user',
                'message_type': 'text',
                'content': 'Hello, how are you?',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'bot',
                'message_type': 'text',
                'content': 'I am fine, thank you.',
            },
            {
                'conversation_id': conversation_1.id,
                'role': 'user',
                'message_type': 'video',
                'file_path': 'https://st2.depositphotos.com/40853472/44728/v/600/depositphotos_447280567-stock-video-portrait-of-a-female-doctor.mp4',
            },
        ]:
            await container.message_service().create(
                db=db,
                req=MessageCreateRequest(**message_data),
            )
        print('Successfully setup data')


if __name__ == '__main__':
    import asyncio

    asyncio.run(setup_data())
