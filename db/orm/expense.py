from db.models import session, Expense
from variables import ROW_COUNT
from datetime import datetime


def create(name: str, cost: float, date: datetime) -> Expense:
    expense = Expense(name, cost, date)
    session.add(expense)
    session.commit()
    return expense


def edit(id: int, name: str, cost: float, date: datetime) -> Expense | None:
    expense: Expense | None = session.query(Expense).filter(Expense.id == id).scalar()
    if not expense:
        return None
    expense.name = name
    expense.cost = cost
    expense.date = date
    session.commit()
    return expense


def del_res(id: int) -> bool:
    expense: Expense | None = session.query(Expense).filter(Expense.id == id).scalar()
    if not expense:
        return False
    expense.is_enabled = not expense.is_enabled
    session.commit()
    return True


def get_by_id(id: int) -> Expense | None:
    expense = session.query(Expense).filter(Expense.id == id).scalar()
    return expense


def get_paginated(page: int, show_deleted: bool = False) -> tuple[list[Expense], int]:
    expenses = session.query(Expense).order_by(Expense.date.desc())
    if not show_deleted:
        expenses = expenses.filter(Expense.is_enabled.is_(True))
    count: int = expenses.count()
    paginated_expenses: list[Expense] = expenses.slice((page - 1) * ROW_COUNT, page * ROW_COUNT)
    return paginated_expenses, count
