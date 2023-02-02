import uvicorn
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware

from core.api.user.router import user_router
from fastapi_sqlalchemy import db

DB_URL = 'mysql+pymysql://root:test@localhost:3306/account_book_api?charset=utf8'
app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=DB_URL)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
