from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from database.crud import crud_register_user, crud_login_user
from schemas.user import UserLoginSchema, UserResponseSchema
from exceptions import UserAlreadyExists, UserNotExists, UserIncorrectPassword


router = APIRouter(prefix='/auth')

@router.post('/register', response_model=UserResponseSchema)
def register_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        new_user = crud_register_user(db=db, user=user)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email: {user.email} already exists')

    return new_user

@router.post('/login', response_model=UserResponseSchema)
def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        get_user = crud_login_user(db=db, user=user)
    except UserNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user.email} not found")
    except UserIncorrectPassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect password')

    return get_user