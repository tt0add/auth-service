from sqlalchemy.orm import Session
from schemas.user import UserLoginSchema
import database.models as models
from utils.hashing import hash_password, verify_password
from exceptions import UserAlreadyExists, UserNotExists, UserIncorrectPassword


def crud_register_user(db: Session, user: UserLoginSchema):
    get_user = db.query(models.User).filter(models.User.email == user.email).first()

    if get_user:
        raise UserAlreadyExists()

    hashed_password = hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password, role='user')

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def crud_login_user(db: Session, user: UserLoginSchema):
    get_user = db.query(models.User).filter(models.User.email == user.email).first()

    if get_user is None:
        raise UserNotExists()
    
    if verify_password(user.password, get_user.password):
        return get_user
    else:
        raise UserIncorrectPassword()
