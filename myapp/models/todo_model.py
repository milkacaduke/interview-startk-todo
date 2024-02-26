from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import uuid

""" 
Todo Models and Schemas
"""
class Comment(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    message: str

class Todo(Document):
    title: str
    message: str
    comments: Optional[List[Comment]] = []

    class Settings:
        name = "todos"

class UpdateTodo(BaseModel):
    title: str | None
    message: str | None
