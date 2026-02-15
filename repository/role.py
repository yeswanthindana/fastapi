from fastapi import Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

def create_role(request: schemas.Role, db: Session = Depends(get_db)):
    required_fields = ["name", "description"]
    for field in required_fields:
        if not getattr(request, field):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing required field: {field}")

    if db.query(models.role).filter(models.role.name == request.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    
    new_role = models.role(name=request.name.strip(), description=request.description.strip())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {
        "message": "Role successfully created",
        "id" : new_role.id,
        "data": new_role
    }
    

def delete_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role_obj = db.query(models.role).filter(models.role.id == role_id).first()
    if not role_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} not found")
    db.delete(role_obj)
    db.commit()
    return {"message": f"Role id with {role_obj.name} of id {role_id} is deleted successfully"}


def update_role_by_id(role_id: int, request: schemas.Role, db: Session = Depends(get_db)):
    role_obj = db.query(models.role).filter(models.role.id == role_id).first()
    if not role_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} not found")
    
    role_obj.name = request.name.strip()
    role_obj.description = request.description.strip()
    db.commit()
    db.refresh(role_obj)
    return {
        "message": "Role successfully updated",
        "id" : role_obj.id,
        "data": role_obj
    }

def get_all_roles(db: Session = Depends(get_db)):
    roles = db.query(models.role).all()
    return {
        "message": "Roles successfully retrieved",
        "data": roles
    }

def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role_obj = db.query(models.role).filter(models.role.id == role_id).first()
    if not role_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} not found")
    return {
        "message": "Role successfully retrieved",
        "id" : role_obj.id,
        "data": role_obj
    }
