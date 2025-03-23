from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserBase, UserResponse, UpdatePasswordRequest, UserDeleteRequest
from utils import hash_password, verify_password
from models.user import User
from utils import get_current_user
from database import get_db

router = APIRouter()

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



@router.put("/update", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_update: UserBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure current_user exists
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if email is already taken (Excluding current user)
    existing_user = db.query(User).filter(
        User.email == user_update.email, User.id != current_user.id
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use.")

    # Update user details
    current_user.username = user_update.username
    current_user.email = user_update.email

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return UserResponse(id=current_user.id, username=current_user.username, email=current_user.email)


@router.put("/update-password", status_code=status.HTTP_200_OK)
def update_password(
    password_data: UpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify old password
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password.")

    # Hash new password & update
    current_user.password_hash = hash_password(password_data.new_password)
    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return {"message": "Password updated successfully!"}

@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_user(
    password_data: UserDeleteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Warning Message (Before Deletion)
    warning_message = {
        "warning": "⚠️ Once deleted, you will need to register again to access the system.",
        "confirmation": "If you still want to proceed, enter your password."
    }

    # Verify password before deletion
    if not verify_password(password_data.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password.")

    # Proceed with deletion
    db.delete(current_user)
    db.commit()

    return {
        "message": "Account deleted successfully!",
        "info": "You will need to register again to access the system."
    }
