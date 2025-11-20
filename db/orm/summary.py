from sqlalchemy import func
from db.models import session, Income, Expense, Credit
from datetime import date
from template import number_seperator
from variables import SERVICE_TYPES


def total_expense(from_: date | None = None, to_: date | None = None) -> str:
    expenses = session.query(func.sum(Expense.cost)).filter(Expense.is_enabled.is_(True))
    if from_:
        expenses = expenses.filter(func.DATE(Expense.date) >= from_)
    if to_:
        expenses = expenses.filter(func.DATE(Expense.date) <= to_)
    total = expenses.scalar() or 0
    return number_seperator(total)


def total_income(from_: date | None = None, to_: date | None = None) -> str:
    incomes = session.query(func.sum(Income.price)).filter(Income.is_enabled.is_(True))
    if from_:
        incomes = incomes.filter(func.DATE(Income.date) >= from_)
    if to_:
        incomes = incomes.filter(func.DATE(Income.date) <= to_)
    total = incomes.scalar() or 0
    return number_seperator(total)


def remaining_credit() -> str:
    remaining_credit = session.query(func.sum(Credit.current_amount)).scalar() or 0
    return number_seperator(remaining_credit)


def current_capital() -> str:
    total_income = session.query(func.sum(Income.price)).filter(Income.is_enabled.is_(True)).scalar() or 0
    total_expense = session.query(func.sum(Expense.cost)).filter(Expense.is_enabled.is_(True)).scalar() or 0
    total_current_credit = session.query(func.sum(Credit.initial_amount)).scalar() or 0
    paid_credit = total_current_credit - (session.query(func.sum(Credit.current_amount)).scalar() or 0)
    current_amount = total_income - (total_expense - total_current_credit) - paid_credit
    return number_seperator(current_amount)


def income_by_type(from_: date | None = None, to_: date | None = None) -> list[str]:
    incomes = session.query(Income).filter(Income.is_enabled.is_(True))
    if from_:
        incomes = incomes.filter(func.DATE(Income.date) >= from_)
    if to_:
        incomes = incomes.filter(func.DATE(Income.date) <= to_)
    total = [0 for _ in SERVICE_TYPES]
    no_of_entry = [0 for _ in SERVICE_TYPES]
    for income in incomes:
        i = -1
        entry_list = [income_list.split("::") for income_list in income.income_list.split("||")]
        for entry, price in entry_list:
            i = i if service_type_index(entry) == -1 else service_type_index(entry)
            total[i] += float(price)
            no_of_entry[i] += 1
        total[i] -= income.discount
    return [f"{number_seperator(type_total)}/{count}" for type_total, count in zip(total, no_of_entry)]


def service_type_index(entry: str):
    for i, s_type in enumerate(SERVICE_TYPES.values()):
        if s_type in entry:
            return i
    return -1
