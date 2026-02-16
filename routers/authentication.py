from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
import schemas, models, jwt_token
from sqlalchemy.orm import Session
from database import get_db
from hash import Hash
import repository.authentication as authentication
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Login

router = APIRouter(prefix="/auth",tags=["Authentication"])



@router.post("/login", status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Token)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    """
    Login with email and password
    """
    return authentication.login(request, db)


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED,response_model_include=["message"])
def logout(request: schemas.Logout, db: Session = Depends(get_db)):
    """
    Logout with email and password
    """
    return authentication.logout(request, db)


@router.post("/forgotpassword", status_code=status.HTTP_202_ACCEPTED,response_model_include=["message"])    
def forgotpassword(request: schemas.forgotpassword, db: Session = Depends(get_db)):
    """
    Forgot password with email
    """
    return authentication.forgotpassword(request, db)    


@router.post("/resetpassword", status_code=status.HTTP_202_ACCEPTED,response_model_include=["message"])    
def resetpassword(request: schemas.resetpassword, db: Session = Depends(get_db)):
    """
    Reset password with email
    """
    return authentication.resetpassword(request, db)    

@router.post("/changepassword", status_code=status.HTTP_202_ACCEPTED,response_model_include=["message"])
def changepassword(request: schemas.changepassword, db: Session = Depends(get_db)):
    """
    Change password with email
    """
    return authentication.changepassword(request, db)