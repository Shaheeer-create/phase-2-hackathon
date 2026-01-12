from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from .config import settings
import urllib.parse

# For PostgreSQL (Neon), we need to ensure the connection has proper SSL settings
database_url_encoded = settings.database_url

# Only add SSL parameters for PostgreSQL connections
if database_url_encoded.startswith("postgresql"):
    if "sslmode=" not in database_url_encoded:
        # Add SSL parameters required for Neon if not already present
        if "?" in database_url_encoded:
            database_url_encoded += "&sslmode=require"
        else:
            database_url_encoded += "?sslmode=require"

# Create the database engine with appropriate settings
# Use different settings for SQLite vs PostgreSQL
if database_url_encoded.startswith("sqlite"):
    engine = create_engine(
        database_url_encoded,
        echo=settings.debug,  # Set to True to see SQL queries in logs
    )
else:
    engine = create_engine(
        database_url_encoded,
        echo=settings.debug,  # Set to True to see SQL queries in logs
        pool_pre_ping=True,  # Verify connections before use
        pool_size=5,  # Adjust pool size for Neon
        max_overflow=10,  # Allow some overflow connections
        pool_recycle=300,  # Recycle connections every 5 minutes
        pool_timeout=30,  # Timeout for getting connection from pool
    )


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Session: A SQLModel database session
    """
    with Session(engine) as session:
        yield session