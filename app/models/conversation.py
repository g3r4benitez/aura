from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    id_conversation: str = Field(default=None, primary_key=True)
    question: str
    answer: str
    sequences_conversation: float
    id_tag: int