from sqlalchemy.orm import Session
from schemas.user import UserCreateSchema, UserResponseSchema
import database.models as models
from utils.hashing import hash_password, verify_password
from exceptions import UserAlreadyExists


def crud_register_user(db: Session, user: UserCreateSchema):
    get_user = db.query(models.User).filter(models.User.email == user.email).first()
    if get_user:
        raise UserAlreadyExists()

    hashed_password = hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password, role='user')

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user