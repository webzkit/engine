from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from core.security import get_password_hash, verify_password
from .base import CRUDBase

from models.user import UserModel
from schemas.user import CreateUserSchema, UpdateUserSchema


class CRUDUser(CRUDBase[UserModel, CreateUserSchema, UpdateUserSchema]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        try:
            return db.query(UserModel).filter(UserModel.email == email).first()
        except SQLAlchemyError as e:
            # todo store to log
            return None

    def create(self, db: Session, *, obj_in: CreateUserSchema) -> Optional[UserModel]:
        try:
            db_obj = UserModel(
                email=obj_in.email,
                hashed_password=get_password_hash(obj_in.password),
                full_name=obj_in.full_name,
                is_superuser=obj_in.is_superuser,
                user_group_id=obj_in.user_group_id,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

            return db_obj
        except SQLAlchemyError as e:
            # todo store to log
            return None

    def update(
        self, db: Session, *, db_obj: UserModel, obj_in: Union[UpdateUserSchema, Dict[str, Any]]
    ) -> Optional[UserModel]:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            if "email" in update_data:
                del update_data["email"]

            if "password" in update_data:
                hashed_password = get_password_hash(update_data["password"])
                del update_data["password"]
                update_data["hashed_password"] = hashed_password

            return super().update(db, db_obj=db_obj, obj_in=update_data)
        except SQLAlchemyError as e:
            # todo store to log
            return None

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[UserModel]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser


user_crud = CRUDUser(UserModel)
