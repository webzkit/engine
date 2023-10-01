from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from .base import CRUDBase

from models.token import TokenModel
from schemas.token import CreateTokenSchema, UpdateTokenSchema


class CRUDToken(CRUDBase[TokenModel, CreateTokenSchema, UpdateTokenSchema]):
    def get_by_access_token(self, db: Session, *, access_token: str) -> Optional[TokenModel]:
        try:
            return db.query(TokenModel).filter(TokenModel.access_token == access_token).first()
        except SQLAlchemyError as e:
            # todo store to log
            print(e)
            return None


token_crud = CRUDToken(TokenModel)
