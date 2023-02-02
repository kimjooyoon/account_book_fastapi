from typing import Union
from fastapi import Header
from fastapi.routing import APIRouter
from fastapi_sqlalchemy import db
from pymysql.err import IntegrityError
from core.api.user.models import User
from core.api.user.schema import UserCreate, UserLogin

from core.util.auth_jwt import *

user_router = APIRouter()


@user_router.post("/users")
async def user_create(
        req: UserCreate,
):
    try:
        created_user = User()
        created_user.email = req.email
        created_user.password = req.password
        check, message = created_user.verify()
        if not check:
            return {"message": message}

        created_user.password = createHashPassword(created_user.password)

        db.session.add(created_user)
        db.session.commit()

        db.session.refresh(created_user)  # update user_id
        return {"id": created_user.id}
    except Exception as IntegrityError:
        db.session.rollback()
        if "Duplicate" in str(IntegrityError):
            return {"message": "중복된 이메일입니다."}
        return {"message": "서버 에러입니다."}


@user_router.post("/login")
async def login(
        req: UserLogin,
):
    try:
        query = db.session.query(
            User.email, User.id, User.password
        ).first()

        verify = pwcheck(req.password, query.password)
        if verify:
            return createToken(query.id, query.email)
        else:
            return {"status": "fail"}
    except IntegrityError:
        db.session.rollback()
        if "duplicate" in str(IntegrityError):
            return {"message": "중복된 이메일입니다."}
        return {"message": "서버 에러입니다."}


@user_router.get("/claims")
async def getClaims(
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        return decode(token)
    else:
        return {"result": "fail"}
