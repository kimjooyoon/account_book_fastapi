from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from core.api.account_books.models import AccountBook

Base = declarative_base()
now = datetime.datetime.utcnow


class AccountBook(Base):
    __tablename__ = 'account_books_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_book_id = Column(Integer, ForeignKey(AccountBook.id), index=True)
    memo = Column(String(400), nullable=False)
    update_at = Column(DateTime(timezone=True), default=now, onupdate=now)
    delete_at = Column(DateTime(timezone=True))
