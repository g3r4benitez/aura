from sqlmodel import Session, select, or_

from app.entities.conversations import ConversationsFilterDTO
from app.models.conversation import Conversation
from app.core.database import engine
from app.services.tag_service import tag_service
from app.core.logger import logger

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
        statement = select(Conversation)

        # look up for tags
        conditions = []
        for tag_value in params.tags.split(","):
            tag = tag_service.find_tag(tag_value.strip())
            if tag:
                conditions.append(Conversation.id_tag == tag.id_tag)
            else:
                logger.info(f"tag with '{tag_value}' doesn't include in look up for conversations"
                            f"because, these doesn't exists ")

        if conditions:
            statement = statement.where(or_(*conditions))

        # look up for company
        # @todo: doesn't exist relation between company and conversations

        results = self.session.exec(statement)
        conversations = results.all()

        if conversations:
            conversations_ids = [conversation.id_conversation for conversation in conversations]
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

