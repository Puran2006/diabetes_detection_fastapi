from sqlalchemy import Column, Integer, String
from ..database import Base  # Import SQLAlchemy Base

# SQLAlchemy User Model (Database Table)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

