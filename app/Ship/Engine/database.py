from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./flower.db")

# Convert asyncpg URL to sync for SQLAlchemy if it's PostgreSQL
if "postgresql+asyncpg://" in DATABASE_URL:
    SYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
else:
    SYNC_DATABASE_URL = DATABASE_URL

# SQLite specific configuration
if SYNC_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SYNC_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SYNC_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()