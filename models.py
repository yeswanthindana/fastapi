from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    updated_by = Column(Integer, nullable=True)
    users = relationship("user", back_populates="org_info")

class role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    created_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    updated_by = Column(Integer, nullable=True)
    users = relationship("user", back_populates="role_info")

class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=True)
    phonenumber = Column(String(20), nullable=True)
    photo = Column(String(255), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    is_verified = Column(Boolean, default=False)
    failed_login_attempts = Column(Integer, default=0)
    created_by = Column(Integer, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    last_activity_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)
    password_updated_at = Column(DateTime, nullable=True)
    password_reset_requested = Column(Boolean, default=False)

    org_info = relationship("organization", back_populates="users")
    role_info = relationship("role", back_populates="users")