import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env file
load_dotenv()

# Fetch the DATABASE_URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

# Create engine
engine = create_engine(DATABASE_URL)

# Session local setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Create tables in the database
Base.metadata.create_all(bind=engine)
