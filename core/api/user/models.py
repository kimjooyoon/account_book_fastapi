from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
import re

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def verify(self):
        c = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        b_email = bool(c.match(self.email))
        if not b_email :
            return False, "이메일 형식이 올바르지 않습니다."
        c = re.compile('^.{4,30}$')
        b_email = bool(c.match(self.email))
        if not b_email :
            return False, "이메일은 최소 4자 부터 30자 입니다."
        b_pw = bool(c.match(self.password))
        if not b_pw :
            return False, "비밀번호는 최소 4자 부터 30자 입니다."
        return True, ""
