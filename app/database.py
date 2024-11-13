from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

# SQLAlchemy's connection URL
# The URL format is: "postgresql+psycopg2://username:password@host:port/database_name"
connection_url = get_settings().DATABASE_URL

# Create an SQLAlchemy engine to connect to the PostgresSQL database.
engine = create_engine(
    connection_url,
    echo=True  # Setting this to True will print SQL statements for testing purposes. Not recommended for deployment
)

# Create a base class for declarative SQLAlchemy models.
Base = declarative_base()

# Create a session-maker to create database sessions.
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Here, you've set up the basic components for interacting with the PostgresSQL database:
# - `engine` to connect to the database
# - `Base` as the base class for declarative models
# - `Session` to create database sessions


# Dependency that creates a new database session for each request and closes it when done
# Here, you're directly returning the session for gRPC usage.
def get_db():
    db = session()
    try:
        return db  # Directly return the session
    finally:
        db.close()  # Close the session after use
