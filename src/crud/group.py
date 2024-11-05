from fastcrud import FastCRUD
from schemas.group import (
    GroupCreateInternal,
    GroupUpdate,
    GroupUpdateInternal,
    GroupDelete,
)
from models.group import Group

CRUDGroup = FastCRUD[
    Group, GroupCreateInternal, GroupUpdate, GroupUpdateInternal, GroupDelete
]

crud_group = CRUDGroup(Group)
