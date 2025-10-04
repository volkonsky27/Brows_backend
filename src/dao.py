from src.database import connection
from models.models import User, Transaction
from sqlalchemy import select
from datetime import datetime


class DatabaseDAO:
    @classmethod
    @connection
    async def add_user_to_db(
        cls, session, telegram_id: int, username: str, first_name: str, last_name: str
    ):
        new_user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(new_user)
        await session.commit()

    @classmethod
    @connection
    async def get_users(cls, session):
        statement = select(User)
        users = await session.execute(statement)
        return users.scalars().all()

    @classmethod
    @connection
    async def get_user(cls, session, telegram_id: int):
        statement_user = select(
            User.username, User.first_name, User.last_name, User.balance
        ).where(User.telegram_id == telegram_id)
        user = await session.execute(statement_user)
        user = user.mappings().first()
        if not user:
            return None
        return user

    @classmethod
    @connection
    async def get_user_transactions(cls, session, telegram_id: int):
        statement = (
            select(Transaction.date, Transaction.sum_op)
            .where(Transaction.telegram_id == telegram_id)
            .order_by(Transaction.date.desc())
            .limit(10)
        )
        result = await session.execute(statement)
        result = result.mappings().all()
        return result

    @classmethod
    @connection
    async def transaction(cls, session, telegram_id: int, sum: int):
        statement = select(User).where(User.telegram_id == telegram_id)
        result = await session.scalars(statement)
        user = result.first()
        if not user:
            raise AttributeError("Нет такого пользователя")
        if (
            sum < 0 and user.__dict__["balance"] < sum * -1
        ):  # Проверим на баланс для списания
            raise ValueError("Недостаточно средств")
        user.balance += sum
        transaction = Transaction(
            date=datetime.now(), telegram_id=telegram_id, sum_op=sum
        )
        session.add(transaction)
        await session.commit()
        return True
