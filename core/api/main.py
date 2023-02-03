import uvicorn
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware

from core.api.user.router import user_router
from core.api.user.models import Base as User_base
from core.api.account_books.models import Base as Book_base
from fastapi_sqlalchemy import db

# 단순 schema.py => database migration 용도 입니다.
from sqlalchemy import create_engine

DB_URL = 'mysql+pymysql://root:test@localhost:3306/account_book_api?charset=utf8'
app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=DB_URL)

engine = create_engine(DB_URL)
User_base.metadata.create_all(bind=engine)
Book_base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
