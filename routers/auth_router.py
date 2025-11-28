from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from database.crud import crud_register_user
from schemas.user import UserCreateSchema, UserResponseSchema
from exceptions import UserAlreadyExists


router = APIRouter(prefix='/auth')

@router.post('/register', response_model=UserResponseSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    try:
        new_user = crud_register_user(db=db, user=user)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email: {user.email} already exists')

    return new_user