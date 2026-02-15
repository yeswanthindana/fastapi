from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
import schemas, models, jwt_token
from sqlalchemy.orm import Session
from database import get_db
from hash import Hash

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

# def login(request: schemas.Login, db: Session = Depends(get_db)):
#     user = db.query(models.user).filter(models.user.email == request.email).first()

@router.post("/login", response_model=schemas.Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses 'username' field for the login identifier (which is email in our case)
    user = db.query(models.user).filter(models.user.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Email Id")
    
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")

    access_token = jwt_token.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
