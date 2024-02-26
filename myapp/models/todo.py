from beanie import Document
from pydantic import BaseModel
from typing import List, Optional

class Comment(Document):
    comment: str

class Todo(Document):
    title: str
    message: str
    # comments: Optional[List[Comment]] = None

    class Settings:
        name = "starbucks"

    class Config:
        schema_extra = {
            "example": {
                "title": "Title for todo",
                "message": "Message part for todo"
            }
        }

class UpdateTodo(BaseModel):
    title: str | None
    message: str | None
