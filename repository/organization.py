from fastapi import Depends, status, HTTPException, Path
from sqlalchemy.orm import Session
import models, schemas
from database import get_db

def create_organization(request: schemas.Organization, db: Session = Depends(get_db)):
    required_fields = ["name", "description"]
    for field in required_fields:
        if not getattr(request, field):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing required field: {field}")

    if db.query(models.organization).filter(models.organization.name == request.name).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organization with this name already exists")
    
    new_org = models.organization(name=request.name.strip(), description=request.description.strip())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return {
        "message": "Organization successfully created",
        "data": new_org
    }
    
def get_all_organizations(db: Session = Depends(get_db)):
    orgs = db.query(models.organization).all()
    return {
        "message": "Organizations successfully retrieved",
        "data": orgs
    }

def get_organization_by_id(organization_id: int, db: Session = Depends(get_db)):
    org = db.query(models.organization).filter(models.organization.id == organization_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with id {organization_id} not found")
    return {
        "message": "Organization successfully retrieved",
        "data": org
    }

def update_organization_by_id(organization_id: int, request: schemas.Organization, db: Session = Depends(get_db)):
    org = db.query(models.organization).filter(models.organization.id == organization_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with id {organization_id} not found")
    
    org.name = request.name.strip()
    org.description = request.description.strip()
    db.commit()
    db.refresh(org)
    return {
        "message": "Organization successfully updated",
        "data": org
    }
    
def delete_organization_by_id(organization_id: int, db: Session = Depends(get_db)):
    org = db.query(models.organization).filter(models.organization.id == organization_id).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization with id {organization_id} not found")
    db.delete(org)
    db.commit()
    return {"message": f"Organization id {organization_id} deleted successfully"}
