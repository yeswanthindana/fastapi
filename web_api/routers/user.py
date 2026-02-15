from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from typing import List

from ..repository import user


router = APIRouter(tags=["Users"], prefix="/user")


@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
#router.post('', status_code=status.HTTP_201_CREATED, response_model_include=["message","data"])
def createuser(request: schemas.User, db: Session = Depends(get_db)):
    """
    Create a new user
    """
    return user.createuser(request, db)

# def get_users(db: Session = Depends(get_db)):

@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.UserSummary])
def get_users(db: Session = Depends(get_db)):
    #def get_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    """
    Get all users with id, email and firstname only
    """
    return user.get_users(db)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(user_id: int = Path(..., gt=0, description="User ID must be a positive integer"), db: Session = Depends(get_db)):
    #def get_user(user_id: int = Path(..., gt=0, description="User ID must be a positive integer"), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user))
    """
    Get user by ID
    """
    return user.get_user(user_id, db)


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
def delete_user(user_id: int = Path(..., gt=0, description="User ID must be a positive integer"), db: Session = Depends(get_db)):
    """
    Delete user by ID
    """
    return user.delete_user(user_id, db)