from sqlmodel import Session, select, or_, distinct

from app.core.config import CACHE_TTL
from app.entities.conversations import ConversationsFilterDTO
from app.models.conversation import Conversation, Tag
from app.core.database import engine
from app.core.cache import redis_client, get_key_from_text

class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation: Conversation) -> Conversation:
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get(self, _id):
        obj = self.session.get(Conversation, _id)
        return obj

    def get_all(self):
        statement = select(Conversation)
        results = self.session.exec(statement)
        return results.all()

    def filter(self, params: ConversationsFilterDTO):
        cache_key = get_key_from_text(params.tags)
        cached_converstions_id = redis_client.get(cache_key)

        if cached_converstions_id:
            return {
                "conversations_ids": cached_converstions_id,
                "total": len(cached_converstions_id),
                "page": 1,
                "per_page": len(cached_converstions_id)
            }
        else:
            statement = (select( distinct(Conversation.id_conversation) ).
                         where(Conversation.id_tag==Tag.id_tag))

            # look up for tags
            conditions = []
            for tag_v in params.tags.split(","):
                conditions.append( Tag.tag_value== tag_v.strip())

            if conditions:

                statement = statement.where(or_(*conditions))

            # look up for company
            # @todo: doesn't exist relation between company and conversations

            results = self.session.exec(statement)
            conversations = results.all()

            if conversations:
                conversations_ids = ",".join(map(str,conversations))
                redis_client.setex(cache_key, CACHE_TTL, conversations_ids)
                return {
                    "conversations_ids": conversations_ids,
                    "total": len(conversations_ids),
                    "page": 1,
                    "per_page": len(conversations_ids)
                }
            else:
                return None


session = Session(engine)
conversation_service = ConversationService(session)

