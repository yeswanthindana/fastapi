from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
import schemas
from database import get_db
from typing import List
import repository.organization as organization

router = APIRouter(tags=["Organizations"], prefix="/organization")

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowOrganization)
def create_organization(request: schemas.Organization, db: Session = Depends(get_db)):
    """
    Create a new organization
    """
    return organization.create_organization(request, db)

@router.get("/all", status_code=status.HTTP_200_OK)
def get_all_organizations(db: Session = Depends(get_db)):
    """
    Get all organizations
    """
    return organization.get_all_organizations(db)

@router.get("/{organization_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowOrganization)
def get_organization_by_id(organization_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """
    Get an organization by id
    """
    return organization.get_organization_by_id(organization_id, db)

@router.put("/{organization_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowOrganization)
def update_organization_by_id(organization_id: int = Path(..., gt=0), request: schemas.Organization = None, db: Session = Depends(get_db)):
    """
    Update an organization by id
    """
    return organization.update_organization_by_id(organization_id, request, db)

@router.delete("/{organization_id}", status_code=status.HTTP_200_OK)
def delete_organization_by_id(organization_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """
    Delete an organization by id
    """
    return organization.delete_organization_by_id(organization_id, db)
