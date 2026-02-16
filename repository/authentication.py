from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from hash import Hash
import jwt_token
from fastapi.security import OAuth2PasswordRequestForm
import schemas
import utils


def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Email Id")    
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")    
    if user.password_reset_requested:
        user.password_reset_requested = False
        db.commit()
    access_token = jwt_token.create_access_token(data={"sub": user.email})   
    return {"access_token": access_token, "token_type": "bearer"}

def logout(request: schemas.Logout, db: Session = Depends(get_db)):
    return {"message": "Successfully logged out"}

def forgotpassword(request: schemas.forgotpassword, db : Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Email Id")       
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active")        
    if user.password_reset_requested:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset already requested, please contact admin")
    user.password_reset_requested = True
    db.commit()
    
    return {"message": "Password reset request sent to admin, please contact admin"}

def resetpassword(request: schemas.resetpassword, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    temp_password = utils.generate_random_password()
    user.password = Hash.hash_password(temp_password)
    db.commit()    
    return {
        "message": "Password reset successfully with temporary password", 
        "temporary_password": temp_password
    }

def changepassword(request: schemas.changepassword, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")    
    if not Hash.verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")
    user.password = Hash.hash_password(request.new_password)
    user.password_reset_requested = False
    db.commit()   
    return {"message": "Password successfully changed"}