import os

def get_supabase_db_url():
    """
    Handles Supabase connection string formatting.
    Supabase URIs usually start with 'postgres://', but SQLAlchemy 2.x
    requires 'postgresql://'. We also append '+psycopg' for the driver.
    """
    url = os.getenv("DATABASE_URL")
    
    if not url:
        # Fallback for local development
        return "postgresql+psycopg://postgres:123@localhost:5432/postgres"
    
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
        
    return url
