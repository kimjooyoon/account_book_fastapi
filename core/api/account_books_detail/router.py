from typing import Union
from fastapi import Header
from fastapi.routing import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy.sql.expression import null
from pymysql.err import IntegrityError

from datetime import datetime

from core.util.auth_jwt import *
from core.api.account_books_detail.schema import Memo
from core.api.account_books_detail.models import AccountBookDetail
from core.api.account_books.models import AccountBook

detail_router = APIRouter()


def create_detail(user_id, book_id, memo, money):
    if not is_books_by_id_and_userid(book_id, user_id):
        return 0

    m = AccountBookDetail()
    m.memo = memo
    m.used_money = money
    m.account_book_id = book_id
    db.session.add(m)
    db.session.commit()
    db.session.refresh(m)
    return m.id


def is_books_by_id_and_userid(id, user_id):
    query = db.session.query(
        AccountBook.user_id
    ).where(
        AccountBook.id == id,
        AccountBook.delete_at.is_(null())
    )

    u_id = query.first()
    if u_id is None:
        return False
    if u_id[0] == user_id:
        return True
    return False


def exist_dest_books(dest_date, user_id):
    query = db.session.query(
        AccountBook.id
    ).where(
        AccountBook.dest_date == dest_date,
        AccountBook.user_id == user_id,
        AccountBook.dest_date.is_(null())
    ).first()
    if query is None:
        return False
    return True


@detail_router.post("/accounts/{id}/detail")
async def accounts_create(
        req: Memo,
        money: int = 0,
        id: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        memo = req.memo
        account_id = id

        try:
            detail_id = create_detail(user_id, account_id, memo, money)
            return {detail_id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


def get_detail_by_id(id: int):
    query = db.session.query(
        AccountBookDetail
    ).where(
        AccountBookDetail.id == id,
        AccountBookDetail.delete_at.is_(null())
    )
    detail = query.first()
    return detail


def update_detail(m: AccountBookDetail, memo: str, money):
    m.memo = memo
    m.used_money = money
    db.session.commit()


@detail_router.put("/accounts/detail/{id}")
async def accounts_update(
        req: Memo,
        id: int = 0,
        money: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        memo = req.memo
        detail: AccountBookDetail = get_detail_by_id(id)
        if detail is None:
            return {"result": "해당 가계부가 없습니다."}
        update_detail(detail, memo, money)
        try:
            return {"result": "success"}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


def get_account_detail_list(id, user_id):
    list = db.session.query(
        AccountBookDetail
    ).where(
        AccountBook.user_id == user_id,
        AccountBook.id == id,
        AccountBook.delete_at.is_(null())
    ).all()
    return list


@detail_router.get("/accounts/{id}/detail")
async def accounts_list(
        id: int,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        try:
            return get_account_detail_list(id, user_id)

        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


def delete_detail(id: int):
    m: AccountBookDetail = get_detail_by_id(id)
    m.delete_at = datetime.datetime.today()
    db.session.commit()
    return m.id


def exist_detail_by_id(id, user_id):
    m: AccountBookDetail = get_detail_by_id(id)
    m2: AccountBook = get_account(m.account_book_id, user_id)

    if m.account_book_id == m2.id:
        return True
    return False


def get_account(account_id: int, user_id: int):
    book = db.session.query(AccountBook).where(
        AccountBook.id == account_id,
        AccountBook.user_id == user_id,
        AccountBook.delete_at.is_(null())
    ).first()
    return book


@detail_router.delete("/accounts/detail/{id}")
async def detail_delete(
        id: int,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        if not exist_detail_by_id(id, user_id):
            return {"result": now + ", 해당 일자 가계부 상세정보는 없습니다."}
        try:
            deleted_id = delete_detail(id)
            return {"deleted_id": deleted_id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    return {"result": "fail"}
