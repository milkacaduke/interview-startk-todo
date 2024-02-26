from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from myapp.models.user_model import Token, UserInDB, UserIn, User

router = APIRouter()