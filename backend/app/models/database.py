"""
Database configuration and session management for FloatChat.

Provides SQLAlchemy setup with PostgreSQL support and CSV fallback for development.
"""

from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./floatchat.db")
CSV_FALLBACK = os.getenv("CSV_FALLBACK", "true").lower() == "true"

# SQLAlchemy setup
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class SurfaceData(Base):
    """Surface temperature and salinity measurements."""
    __tablename__ = "surface_data"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    temperature = Column(Float)
    salinity = Column(Float)


class MonthlyAverages(Base):
    """Monthly averaged temperature and salinity by depth."""
    __tablename__ = "monthly_averages"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    lat = Column(Float, index=True)
    lon = Column(Float, index=True)
    depth = Column(Float, index=True)
    temperature = Column(Float)
    salinity = Column(Float)


class HeatContent(Base):
    """Heat content measurements."""
    __tablename__ = "heat_content"
    
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, index=True)
    lat = Column(Float, index=True)
    lon = Column(Float, index=True)
    heat_content = Column(Float)


class FloatMetadata(Base):
    """ARGO float metadata and deployment information."""
    __tablename__ = "float_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    float_id = Column(String(50), unique=True, index=True)
    deployment_date = Column(DateTime)
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String(20))
    last_transmission = Column(DateTime)
    data_summary = Column(Text)  # JSON summary of available measurements


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize tables on import
try:
    create_tables()
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")
    print("Falling back to CSV data mode")