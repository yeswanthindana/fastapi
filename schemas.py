from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# REQUEST & RESPONSE VALIDATION

class User(BaseModel):
    username: str
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    password: str
    firstname: str
    lastname: str 
    role_id: int
    organization_id: int
    phonenumber: Optional[str] = Field(
        default=None,
        pattern=r"^(?:\+91|91)?[6-9]\d{9}$"
    )
    photo: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None


class UserSummary(BaseModel):
    id: int
    email: str
    firstname: str

    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    message: str
    data: User

    class Config:
        from_attributes = True    

class Role(BaseModel):
    name: str
    description : str
    created_at : Optional[datetime] = None
    created_by : Optional[int] = None
    updated_at : Optional[datetime] = None
    updated_by : Optional[int] = None
    

class ShowRole(BaseModel):
    message: str
    id: int
    data: Role
    
    class Config:
        from_attributes = True

class Organization(BaseModel):
    name: str  
    description : str   
    created_at : Optional[datetime] = None
    created_by : Optional[int] = None
    updated_at : Optional[datetime] = None
    updated_by : Optional[int] = None

class ShowOrganization(BaseModel):
    message: str
    id: int
    data: Organization
    
    class Config:
        from_attributes = True


class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Logout(BaseModel):
    email: str
    

class forgotpassword(BaseModel):
    email: str

class resetpassword(BaseModel):
    email : str


class changepassword(BaseModel):
    email : str
    old_password : str
    new_password : str    