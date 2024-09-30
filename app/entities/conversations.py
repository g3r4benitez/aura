from pydantic import BaseModel
from typing import Optional

class ConversationsFilterDTO(BaseModel):
    company: Optional[str] = ""
    tags: Optional[str] = ""
