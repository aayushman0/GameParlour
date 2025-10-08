from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase

from datetime import datetime


BaseModel: DeclarativeBase = declarative_base()


class Income(BaseModel):
    __tablename__ = "income"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    customer_name = Column("customer_name", String, index=True)
    income_list = Column("income_list", String, nullable=False)
    discount = Column("discount", Float)
    price = Column("price", Float)
    date = Column("date", DateTime, index=True)
    is_enabled = Column("is_enabled", Boolean, default=True)

    def __init__(self, customer_name: str, income_list: str, discount: float, price: float, date: datetime | None = None):
        self.customer_name = customer_name
        self.income_list = income_list
        self.discount = discount
        self.price = price
        self.date = date if date else datetime.now()


class Expense(BaseModel):
    __tablename__ = "expense"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, index=True, nullable=False)
    cost = Column("cost", Float)
    date = Column("date", DateTime, index=True)
    is_enabled = Column("is_enabled", Boolean, default=True)

    def __init__(self, name: str, cost: float, date: datetime | None = None):
        self.name = name
        self.cost = cost
        self.date = date if date else datetime.now()


class Credit(BaseModel):
    __tablename__ = "credit"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    provider = Column("provider", String, index=True, nullable=False)
    initial_amount = Column("initial_amount", Float)
    current_amount = Column("current_amount", Float)
    initial_date = Column("initial_date", DateTime)
    last_date = Column("last_date", DateTime)

    def __init__(self, provider: str, initial_amount: float, initial_date: datetime):
        self.provider = provider
        self.initial_amount = initial_amount
        self.current_amount = initial_amount
        self.initial_date = initial_date
        self.last_date = initial_date


class Device(BaseModel):
    __tablename__ = "device"

    name = Column("name", String, primary_key=True)
    is_running = Column("is_running", Boolean)
    start_time = Column("start_time", DateTime, nullable=True)
    max_time = Column("max_time", Integer, nullable=True)

    def __init__(self, name: str, is_running: bool, start_time: datetime | None = None, max_time: int | None = None):
        self.name = name
        self.is_running = is_running
        self.start_time = start_time
        self.max_time = max_time


engine = create_engine("sqlite:///database.db", echo=False)
BaseModel.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
