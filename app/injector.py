from dependency_injector import containers, providers

from app.model import Database
from app.repository.conversation_repository import ConversationRepository
from app.repository.user_repository import UserRepository
from app.service.conversation_service import ConversationService
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


container = Container()

# Usage example
# user_service = container.user_service()
