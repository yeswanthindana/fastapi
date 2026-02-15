from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from supabase_config import get_supabase_db_url

# Use the mapping from supabase_config.py
SQLALCHEMY_DATABASE_URL = get_supabase_db_url()


# SQLALCHEMY_DATABASE_URL = os.getenv(
#     "DATABASE_URL", 
#     "postgresql+psycopg://postgres:123@localhost:5432/postgres"
# )   - before cdocker container fix

# SQLALCHEMY_DATABASE_URL = ( "postgresql://postgres:123@localhost:5432/postgres" ) - before docker

engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,        # connection pool
        max_overflow=20 
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()