
from sqlmodel import Field, SQLModel

class Tag(SQLModel, table=True):
    id_tag: int = Field(default=None, primary_key=True)
    tag_value: str
