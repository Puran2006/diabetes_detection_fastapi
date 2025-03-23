from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from utils import hash_password, verify_password, create_access_token, get_current_user, credentials_exception
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user with a hashed password.",
    tags=["Authentication"]
             )
def register(user: UserCreate, db: Session = Depends(get_db)):
    # check if user already exits or not
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists!"
        )  
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered!"
        )
        # Hash the password before saving
    hashed_pwd = hash_password(user.password)

    # Create new user
    new_user = User(username=user.username, email=user.email, password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return new_user

@router.post("/login", response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and returns access token." ,
    tags=["Authentication"]
    )
def login(form_data: OAuth2PasswordRequestForm = Depends(),  
    db: Session = Depends(get_db)
    ):
    db_user = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise credentials_exception
    access_token = create_access_token({"sub": db_user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.get("/profile",
    status_code=status.HTTP_200_OK,
    summary="Get user profile",
    description="Returns the profile of the authenticated user."
)
def welcome_user(user: User = Depends(get_current_user)):
    return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "message": f"welcome MR : {user.username}"
            }

