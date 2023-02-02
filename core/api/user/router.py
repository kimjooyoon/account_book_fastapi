from fastapi.routing import APIRouter
from fastapi_sqlalchemy import db
from pymysql.err import IntegrityError
from core.api.user.models import User
from core.api.user.schema import UserCreate

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
