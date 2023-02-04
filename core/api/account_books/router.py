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


def update_account_books(account_id, user_id, money):
    m = get_account(account_id, user_id)
    m.used_money = money

    db.session.commit()
    db.session.refresh(m)
    return m.id


def get_account(account_id: int, user_id: int):
    return db.session.query(AccountBook).where(
        AccountBook.id == account_id,
        AccountBook.user_id == user_id
    ).first()


def exist_account_by_id(id: int, user_id: int):
    query = db.session.query(
        AccountBook.id
    ).where(AccountBook.id == id, AccountBook.user_id == user_id).first()
    if query is None:
        return False
    return True


def exist_dest_books(dest_date, user_id):
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
            return {"result": now + ", 일자 가계부는 이미 추가 되었습니다."}
        try:
            id = create_account_books(user_id, now, money)
            return {id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


@account_books_router.post("/accounts/date/{dest_date}")
async def accounts_create(
        dest_date: str,
        money: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        now = dest_date
        if exist_dest_books(now, user_id):
            return {"result": now + ", 일자 가계부는 이미 추가 되었습니다."}
        try:
            id = create_account_books(user_id, now, money)
            return {id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


@account_books_router.put("/accounts/{id}")
async def accounts_update(
        id: int,
        money: int = 0,
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        if not exist_account_by_id(id, user_id):
            return {"result": now + ", 해당 일자 가계부는 없습니다."}
        try:
            id = update_account_books(id, user_id, money)
            return {id}
        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}


def get_account_list(user_id):
    list = db.session.query(AccountBook).where(AccountBook.user_id == user_id).all()
    return list


# URL = /accounts/{:id} GET
@account_books_router.get("/accounts")
async def accounts_list(
        token: Union[str, None] = Header(default=None, convert_underscores=False)
):
    if verify(token):
        user_id = decode(token).get('user_id')
        try:
            return get_account_list(user_id)

        except Exception as IntegrityError:
            return {"result": "system error: " + str(IntegrityError)}
    else:
        return {"result": "fail"}

    return ""
