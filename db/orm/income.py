from db.models import session, Income
from variables import ROW_COUNT
from datetime import datetime


def create(customer_name: str, income_list: str, discount: float, price: float, date: datetime) -> Income:
    income = Income(customer_name, income_list, discount, price, date)
    session.add(income)
    session.commit()
    return income


def edit(id: int, customer_name: str, income_list: str, discount: float, price: float, date: datetime) -> Income | None:
    income: Income | None = session.query(Income).filter(Income.id == id).scalar()
    if not income:
        return None
    income.customer_name = customer_name
    income.income_list = income_list
    income.discount = discount
    income.price = price
    income.date = date
    session.commit()
    return Income


def del_res(id: int) -> bool:
    income: Income | None = session.query(Income).filter(Income.id == id).scalar()
    if not income:
        return False
    income.is_enabled = not income.is_enabled
    session.commit()
    return True


def get_by_id(id: int) -> Income | None:
    income = session.query(Income).filter(Income.id == id).scalar()
    return income


def get_paginated(page: int, show_deleted: bool = False) -> tuple[list[Income], int]:
    incomes = session.query(Income).order_by(Income.date.desc())
    if not show_deleted:
        incomes = incomes.filter(Income.is_enabled.is_(True))
    count: int = incomes.count()
    paginated_incomes: list[Income] = incomes.slice((page - 1) * ROW_COUNT, page * ROW_COUNT)
    return paginated_incomes, count
