from sqlmodel import Session, select
from app.models.conversation import Conversation
from app.core.database import engine

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


session = Session(engine)
conversation_service = ConversationService(session)

