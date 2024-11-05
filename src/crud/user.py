from fastcrud import FastCRUD
from models.user import User
from schemas.user import UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete

CRUDUser = FastCRUD[User, UserCreateInternal, UserUpdate, UserUpdateInternal, UserDelete]

crud_user = CRUDUser(User)
