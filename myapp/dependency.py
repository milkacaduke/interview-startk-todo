from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from myapp.config.config import get_config

from myapp.models.user_model import User, UserIn, UserInDB
from pprint import pprint

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

async def verify_access_token(token: str):
    """ Verify if JWT token in requests is correct """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1. decode token
        token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        """ Sample usage:
            token = jwt.encode({'key': 'value'}, 'secret', algorithm='algo')
            jwt.decode(token, 'secret', algorithms=['algo'])
            {u'key': u'value'} 
        """
        # 2. get username from jwt token subject
        username = token_payload.get("sub")
        if username is None:
            raise credentials_exception
        # 3. get user from db with decoded username
        user = await User.find_one(username == User.username)
        if user is None:
            raise credentials_exception
    
        return user
    except JWTError:
        raise credentials_exception


async def authenticate_user(username: str, password: str):
    user = await User.find_one(User.username == username)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # At this point, user exists and password is verified!
    return user

async def get_current_user(token: str=Depends(oauth2_scheme)):
    """ Dependency - Extracts and verifies user from token """
    return verify_access_token(token)