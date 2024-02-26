from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
import uuid

""" 
User Models and Schemas 
"""
class User(Document):
    username: str
    hashed_password: str

    class Settings:
        name = "users"


class UserInDB(BaseModel):
    """ User data in database. password hashed """
    username: str
    hashed_password: str

class UserIn(BaseModel):
    """ User input. password plain text """
    username: str
    password: str


"""
Token Models
"""
class Token(BaseModel):
    access_token: str
    token_type: str