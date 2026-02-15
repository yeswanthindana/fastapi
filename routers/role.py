from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.orm import Session
import schemas
from database import get_db
from typing import List
import repository.role as role

router = APIRouter(tags=["Roles"], prefix="/role")

#@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowRole)
@router.post('', status_code=status.HTTP_201_CREATED, response_model_include=["message", "id", "data"])
def create_role(request: schemas.Role, db: Session = Depends(get_db)):
    """
    Create a new role
    """
    return role.create_role(request, db)

@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_roles(db: Session = Depends(get_db)):
    """
    Get all roles
    """
    return role.get_all_roles(db)

@router.get('/{role_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowRole)
def get_role_by_id(role_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """
    Get a role by id
    """
    return role.get_role_by_id(role_id, db)

@router.put('/{role_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowRole)
def update_role_by_id(role_id: int = Path(..., gt=0), request: schemas.Role = None, db: Session = Depends(get_db)):
    """
    Update a role by id
    """
    return role.update_role_by_id(role_id, request, db)

@router.delete('/{role_id}', status_code=status.HTTP_200_OK)
def delete_role_by_id(role_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    """
    Delete a role by id
    """
    return role.delete_role_by_id(role_id, db)
