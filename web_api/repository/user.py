from fastapi import Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..hash import Hash

def createuser(request: schemas.User, db: Session = Depends(get_db)):
    """
    Create a new user with validation for role and organization
    """
    required_fields = {
        "username": request.username,
        "email": request.email,
        "password": request.password,
        "firstname": request.firstname,
        "lastname": request.lastname,
        "role_id": request.role_id,
        "organization_id": request.organization_id,
    }

    missing_fields = [k for k, v in required_fields.items() if v is None]
    if missing_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing mandatory fields: {', '.join(missing_fields)}"
        )

    org = db.query(models.organization).filter(models.organization.id == request.organization_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {request.organization_id} does not exist"
        )

    role = db.query(models.role).filter(models.role.id == request.role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {request.role_id} does not exist"
        )


    if db.query(models.user).filter(models.user.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    if db.query(models.user).filter(models.user.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    hashed_password = Hash.hash_password(request.password)

    new_user = models.user(
        username=request.username.strip(),
        email=request.email.lower(),
        password=hashed_password,  
        firstname=request.firstname,
        lastname=request.lastname,
        phonenumber=request.phonenumber,
        photo=request.photo,
        organization_id=request.organization_id,
        role_id=request.role_id,
        is_active=request.is_active if request.is_active is not None else True,
        is_superuser=request.is_superuser if request.is_superuser else False,
        is_verified=request.is_verified if request.is_verified else False,
        created_at=request.created_at,
        updated_at=request.updated_at,
        created_by=request.created_by
   
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User successfully created",
        "id": new_user.id,
        "data": new_user
    }

def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID
    """
    user = db.query(models.user).filter(models.user.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {
        "message": "User retrieved successfully",
        "data": user
    }

def get_users(db: Session = Depends(get_db)):
    """
    Get all users
    """
    users = db.query(models.user).all()
    return users

def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete user by ID
    """
    user = db.query(models.user).filter(models.user.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return {"message": f"User id {user_id} deleted successfully "}