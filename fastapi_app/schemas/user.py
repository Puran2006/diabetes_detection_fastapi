from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# Base User Schema (Common fields)
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Unique username for the user")
    email: EmailStr = Field(description="Valid email address")
    
class UserCreate(UserBase):
    password: str = Field(min_length=6, description="Password (min 6 characters)")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "strongpassword123"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr = Field(description="User email")
    password: str = Field(description="User password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "strongpassword123"
            }
        }

class UserResponse(UserBase):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john.doe@example.com"
            }
        }

class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6, description="Password (min 6 characters)")
    new_password: str = Field(min_length=6, description="Password (min 6 characters)")

class UserDeleteRequest(BaseModel):
    password: str = Field(min_length=6, description="Password (min 6 characters)")

class TokenResponse(BaseModel):
    access_token : str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
                "token_type": "bearer"
            }
        }

