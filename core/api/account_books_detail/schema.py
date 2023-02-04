from pydantic import BaseModel


class Memo(BaseModel):
    memo: str
