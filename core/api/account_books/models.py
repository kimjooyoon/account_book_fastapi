from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import declarative_base
import datetime
from core.api.user.models import User

Base = declarative_base()
now = datetime.datetime.utcnow


class AccountBook(Base):
    __tablename__ = 'account_books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    used_money = Column(Integer, nullable=False)
    dest_date = Column(String(12), nullable=False)
    update_at = Column(DateTime(timezone=True), default=now, onupdate=now)
    delete_at = Column(DateTime(timezone=True))

    def verify(self):
        if self.used_money >= 0:
            return True
        else:
            return False
