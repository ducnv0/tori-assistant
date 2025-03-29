from dependency_injector import containers, providers

from app.model import Database
from app.repository.conversation_repository import ConversationRepository
from app.repository.message_repository import MessageRepository
from app.repository.user_repository import UserRepository
from app.service.chat_service import ChatService
from app.service.conversation_service import ConversationService
from app.service.message_service import MessageService
from app.service.user_service import UserService


# Define Dependency Injection Container
class Container(containers.DeclarativeContainer):
    user_repository = providers.Singleton(UserRepository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    database = providers.Singleton(Database)
    conversation_repository = providers.Singleton(ConversationRepository)
    conversation_service = providers.Factory(
        ConversationService,
        conversation_repository=conversation_repository,
        user_service=user_service,
    )
    message_repository = providers.Singleton(MessageRepository)
    message_service = providers.Factory(
        MessageService,
        message_repository=message_repository,
        conversation_service=conversation_service,
    )
    chat_service = providers.Factory(
        ChatService,
        user_service=user_service,
        conversation_service=conversation_service,
    )


container = Container()

# Usage example
# user_service = container.user_service()
