from typing import Union
from fastapi import Header
from fastapi.routing import APIRouter
from fastapi_sqlalchemy import db
from pymysql.err import IntegrityError

from datetime import datetime

from core.util.auth_jwt import *
from core.api.account_books.models import AccountBook

account_books_router = APIRouter()


def create_account_books(user_id, dest_date, money):
    m = AccountBook()
    m.used_money = money
    m.user_id = user_id
    m.dest_date = dest_date
    db.session.add(m)
    db.session.commit()
    db.session.refresh(m)
    return m.id


def exist_dest_books(dest_date, user_id):
    m = AccountBook()
    query = db.session.query(
        AccountBook.id
    ).where(AccountBook.dest_date == dest_date, AccountBook.user_id == user_id).first()
    if query is None:
        return False
    return True


@account_books_router.post("/accounts")
async def accounts_create(
        money: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        now = datetime.datetime.today().strftime("%Y-%m-%d")
        if exist_dest_books(now, user_id):
            return {"result": now+", 일자 가계부는 이미 추가 되었습니다."}
        try:
            id = create_account_books(user_id, now, money)
            return {id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}
