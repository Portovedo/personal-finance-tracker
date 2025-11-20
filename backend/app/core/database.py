import sys
import os
from sqlalchemy import create_engine, TypeDecorator, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

# Determine the base path for the database
if getattr(sys, 'frozen', False):
    # Running as PyInstaller EXE: Store DB in the same folder as the executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script: Store DB in the project root
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, "finances.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GUID(TypeDecorator):
    """Platform-independent GUID type for SQLite compatibility."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return uuid.UUID(value)
        return value