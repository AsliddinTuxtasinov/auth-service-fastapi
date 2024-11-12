from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import User
from app.schemas.auth_schemas import UserAuthSchema, UserLoginSchema, ResponseLoginSchema, UserSchema
from app.utils.authentication.auth_utils import JWTAuthUtils

auth_utils = JWTAuthUtils()


class UserUtils:
    def __init__(self):
        self._table = User

    def create_user_if_not_exists(self, data: UserAuthSchema, db_session: Session = Depends(get_db)):
        user = db_session.query(self._table).filter(
            (self._table.phone_number == data.phone_number) | (self._table.email == data.email)
        ).first()
        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        new_user = self._table(
            phone_number=data.phone_number,
            email=data.email,
            password=auth_utils.get_hashed_password(password=data.password)
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user

    def login_user(self, data: UserLoginSchema, db_session: Session = Depends(get_db)):

        user = db_session.query(self._table).filter(self._table.phone_number == data.phone_number).first()
        if not user or not auth_utils.verify_password(password=data.password, hashed_pass=user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="phone number or password incorrect")

        user_info = UserSchema.from_orm(user)
        return ResponseLoginSchema(
            user=user_info,
            access=auth_utils.create_access_token(user.id),
            refresh=auth_utils.create_refresh_token(user.id)
        )

    def get_user(self, user_id: str = Depends(auth_utils.decode_access_token), db_session: Session = Depends(get_db)):
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user = db_session.query(self._table).get(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserSchema.from_orm(user)

    def logout_user(self):
        pass

    def change_user_password(self):
        pass
