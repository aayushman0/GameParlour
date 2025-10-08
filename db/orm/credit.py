from db.models import session, Credit
from variables import ROW_COUNT
from datetime import datetime


def create(provider: str, amount: float, date: datetime) -> Credit:
    credit = Credit(provider, amount, date)
    session.add(credit)
    session.commit()
    return credit


def edit(id: int, provider: str, initial_amount: float, current_amount: float, initial_date: datetime, last_date: datetime) -> Credit | None:
    credit: Credit | None = session.query(Credit).filter(Credit.id == id).scalar()
    if not credit:
        return None
    credit.provider = provider
    credit.initial_amount = initial_amount
    credit.current_amount = current_amount
    credit.initial_date = initial_date
    credit.last_date = last_date
    session.commit()
    return credit


def update(id: int, amount: float, date: datetime) -> Credit | None:
    credit: Credit | None = session.query(Credit).filter(Credit.id == id).scalar()
    if not credit:
        return None
    credit.current_amount -= amount
    credit.last_date = date
    session.commit()
    return credit


def delete(id: int) -> None:
    credit: Credit | None = session.query(Credit).filter(Credit.id == id).scalar()
    if not credit:
        return None
    session.delete(credit)
    session.commit()
    return credit


def get_by_id(id: int) -> Credit | None:
    credit: Credit | None = session.query(Credit).filter(Credit.id == id).scalar()
    return credit


def get_paginated(page: int, provider: str | None = None, show_cleared: bool = False) -> tuple[list[Credit], int]:
    credits = session.query(Credit).order_by(Credit.initial_date.desc())
    if provider:
        credits = credits.filter(Credit.provider.icontains(provider))
    if not show_cleared:
        credits = credits.filter(Credit.current_amount > 0)
    count: int = credits.count()
    paginated_credits: list[Credit] = credits.slice((page - 1) * ROW_COUNT, page * ROW_COUNT)
    return paginated_credits, count
