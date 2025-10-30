from pydantic import BaseModel
from typing import Optional
class Posts(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: Optional[str] = None