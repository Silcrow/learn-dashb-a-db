# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://user:password@localhost:5433/mydatabase"

# Create engine
engine = create_engine(DATABASE_URL)

# Session local setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Create tables in the database
Base.metadata.create_all(bind=engine)
