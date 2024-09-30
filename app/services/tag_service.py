from sqlmodel import Session, select

from app.models.conversation import Tag
from app.core.logger import logger
from app.core.database import engine

class TagService:
    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, tag: Tag) -> Tag:
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag

    def get(self, _id):
        obj = self.session.get(Tag, _id)
        return obj

    def find_tag(self, tag_value: str) -> Tag | None:
        statement = select(Tag).where(Tag.tag_value == tag_value)
        results = self.session.exec(statement)
        tag = results.first()
        if tag:
            return tag
        else:
            logger.error(f"Tag with '{tag_value}' doesn't exist")
            return None

session = Session(engine)
tag_service = TagService(session)

