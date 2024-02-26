from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from myapp.config.config import get_config

from myapp.models.user_model import User, UserIn, UserInDB


"""
Secret section
    - Real secrets are loaded with get_config() from .env
    - If no .env provided, default string value will be loaded from config.py
    - .env is excluded from git and docker
"""
SECRET_KEY = get_config().secret_key
ALGORITHM = get_config().algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = get_config().access_token_expire_minutes

""" 
 Password stuff
 """
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(naked_password: str, hasned_password: str) -> bool:
    return pwd_context.verify(naked_password, hasned_password)


"""
Access Token stuff
"""
def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded_jwt = jwt.encode(
        {"sub": username, "exp": expire},
        SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(username: str, password: str):
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # At this point, user exists and password is verified!
    return user