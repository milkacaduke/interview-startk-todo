from fastapi import APIRouter, Depends, HTTPException, status
from myapp.models.user_model import User
from myapp.dependency import get_current_user


router = APIRouter()

@router.get("/me")
async def user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed"
        )
    
    return {
        "username": current_user.username
    }