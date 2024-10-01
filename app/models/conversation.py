from sqlmodel import Field, SQLModel
from typing import Optional

class Tag(SQLModel, table=True):
    id_tag: int = Field(default=None, primary_key=True)
    tag_value: str


class Conversation(SQLModel, table=True):
    id_conversation: str = Field(default=None, primary_key=True)
    question: str
    answer: str
    sequences_conversation: float
    id_tag: Optional[int] = Field(default=None, foreign_key="tag.id_tag")


