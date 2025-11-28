from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from database.db import get_db
from database.crud import crud_register_user, crud_login_user, crud_get_user
from schemas.user import UserLoginSchema, UserResponseSchema
from exceptions import UserAlreadyExists, UserNotExists, UserIncorrectPassword
from utils.jwt import create_access_token, create_refresh_token, decode_jwt
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/auth')

@router.post('/register', response_model=UserResponseSchema)
def register_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        new_user = crud_register_user(db=db, user=user)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User with email: {user.email} already exists')
    

    return new_user

@router.post('/login', response_model=UserResponseSchema, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login_user(response: Response, user: UserLoginSchema, db: Session = Depends(get_db)):
    try:
        get_user = crud_login_user(db=db, user=user)
    except UserNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {user.email} not found")
    except UserIncorrectPassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect password')
    
    access_token = create_access_token({'sub': str(get_user.id)})
    refresh_token = create_refresh_token({'sub': str(get_user.id)})



    response.set_cookie(key='access_token',
                        value=access_token,
                        httponly=True,
                        secure=False,
                        max_age=60*30)
    
    response.set_cookie(key='refresh_token',
                        value=refresh_token,
                        httponly=True,
                        secure=False,
                        max_age=60*60*24*7)

    return get_user

@router.post('/refresh')
def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Refresh token is missing')
    
    payload = decode_jwt(refresh_token)

    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token type')
    
    user_id = payload.get('sub')

    new_access_token = create_access_token({'sub': user_id})

    response.set_cookie(key='access_token',
                        value=new_access_token,
                        httponly=True,
                        secure=False,
                        max_age=60*30)
    
    return {'detail': 'Access token refreshed'}


@router.get('/me', response_model=UserResponseSchema)
def get_user(request: Request, response: Response, db: Session = Depends(get_db)):
    access_token = request.cookies.get('access_token')

    if not access_token:
        refresh_access_token(request, response)

    payload = decode_jwt(access_token)

    user_id = payload['sub']

    try:
        user = crud_get_user(db=db, user_id=user_id)
    except UserNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with ID: {user_id} not exists (probably db error)')


    return user

@router.post('/logout')
def logout(response: Response):
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return {'detail': 'Logout'}
