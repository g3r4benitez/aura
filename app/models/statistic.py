from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel

class Statistic(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    path: str
    status_code: int
    seconds: float

