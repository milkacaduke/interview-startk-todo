from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from myapp.dependency import authenticate_user, create_access_token, hash_password, get_current_user
from myapp.models.user_model import Token, UserInDB, UserIn, User

router = APIRouter()

@router.post("/register", response_model=UserInDB, tags=["Auth"])
async def register_user(user_input: UserIn):
    """ Handles register user and hash password to store in DB """
    # user input is verified by pydantic.
    # at this point we can assume all input are valid and sanitized
    
    hashed_password = hash_password(user_input.password)
    # Create user
    user = User(username=user_input.username, hashed_password=hashed_password)
    userInDB = UserInDB(username=user.username, hashed_password=user.hashed_password)

    # Insert user into DB
    await user.insert()
    return userInDB


@router.post("/token", response_model=Token, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Handles authenticate user, create and return token user client """
    print("login called")
    
    user = await authenticate_user(form_data.username, form_data.password)
    access_token = create_access_token(user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh():
    ## TODO
    return None