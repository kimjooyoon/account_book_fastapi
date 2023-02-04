from typing import Union
from fastapi import Header
from fastapi.routing import APIRouter
from fastapi_sqlalchemy import db
from pymysql.err import IntegrityError

from datetime import datetime

from core.util.auth_jwt import *
from core.api.account_books_detail.schema import Memo
from core.api.account_books_detail.models import AccountBookDetail
from core.api.account_books.models import AccountBook

detail_router = APIRouter()


def create_detail(user_id, book_id, memo):
    if not is_books_by_id_and_userid(book_id, user_id):
        return 0

    m = AccountBookDetail()
    m.memo = memo
    m.account_book_id = book_id
    db.session.add(m)
    db.session.commit()
    db.session.refresh(m)
    return m.id


def is_books_by_id_and_userid(id, user_id):
    query = db.session.query(
        AccountBook.user_id
    ).where(AccountBook.id == id).first()
    if query is None:
        return False
    if query[0] == user_id:
        return True
    return False


def exist_dest_books(dest_date, user_id):
    query = db.session.query(
        AccountBook.id
    ).where(AccountBook.dest_date == dest_date, AccountBook.user_id == user_id).first()
    if query is None:
        return False
    return True


@detail_router.post("/accounts/{id}/detail")
async def accounts_create(
        req: Memo,
        id: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        memo = req.memo
        account_id = id

        try:
            detail_id = create_detail(user_id, account_id, memo)
            return {detail_id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


def get_detail_by_id(id):
    detail = db.session.query(
        AccountBookDetail
    ).where(AccountBookDetail.id == id).first()
    return detail


def update_detail(m: AccountBookDetail, memo: str):
    m.memo = memo
    db.session.commit()


@detail_router.put("/accounts/detail/{id}")
async def accounts_update(
        req: Memo,
        id: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        memo = req.memo
        detail: AccountBookDetail = get_detail_by_id(id)
        if detail is None:
            return {"result": "해당 가계부가 없습니다."}
        update_detail(detail, memo)

        account_id = id

        try:
            detail_id = create_detail(user_id, account_id, memo)
            return {detail_id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}
