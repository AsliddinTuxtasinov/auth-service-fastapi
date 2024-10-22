from uuid import uuid4

from sqlalchemy import Column, String, DateTime, func, Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))  # UUID as string
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Storing the hashed password
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp when user is created
    is_verified = Column(Boolean, default=False)
