import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import BIGINT, String, Integer, DateTime
from typing import Optional
from src.database import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BIGINT(), primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    balance: Mapped[int] = mapped_column(Integer(), default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime())
    telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    sum_op: Mapped[int] = mapped_column(Integer())
