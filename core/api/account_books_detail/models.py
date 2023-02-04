from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
import datetime
from core.api.account_books.models import AccountBook

Base = declarative_base()
now = datetime.datetime.utcnow


class AccountBookDetail(Base):
    __tablename__ = 'account_books_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_book_id = Column(Integer, ForeignKey(AccountBook.id), index=True)
    used_money = Column(Integer, nullable=False)
    memo = Column(String(110), nullable=False)
    update_at = Column(DateTime(timezone=True), default=now, onupdate=now)
    delete_at = Column(DateTime(timezone=True))

    def verify(self):
        if len(self.memo) > 100:
            return False
        else:
            return True
