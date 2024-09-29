from app.models.conversation import Conversation
from app.repositories.base_respository import BaseRepository

class ConversationRepository(BaseRepository):
    model_name = Conversation


conversation_repository = ConversationRepository()