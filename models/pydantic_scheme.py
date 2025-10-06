import datetime
from pydantic import BaseModel
from typing import Optional


class ShortTransactions(BaseModel):
    date: datetime.datetime
    sum_op: int


class Transactions(ShortTransactions):
    telegram_id: int
    id: int


class User(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None


class Users(User):
    balance: int


class UserInfo(BaseModel):
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    balance: int
    transactions: list[ShortTransactions]


class UserTrans(BaseModel):
    telegram_id: int
    sum: int


class UserTlg(BaseModel):
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    balance: int