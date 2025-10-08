from tkinter import ttk, StringVar
from db.orm import summary
from datetime import date
from template import Frame, DateClass, datetime_entry


class SummaryFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.date_start = DateClass()
        self.date_end = DateClass()
        self.total_expense = StringVar()
        self.total_income = StringVar()
        self.remaining_credit = StringVar()
        self.current_capital = StringVar()

    def main(self):
        self.add_frame.destroy()
        self.detail_frame.destroy()
        self.list_frame.destroy()
        self.left_frame = ttk.Frame(self)
        self.left_frame.columnconfigure(1, weight=1)
        self.left_frame.place(relx=0, rely=0, relwidth=0.35, relheight=1.0)
        self.right_frame = ttk.Frame(self, padding=(50, 0))
        self.right_frame.place(relx=0.35, rely=0, relwidth=0.65, relheight=1.0)

        ttk.Label(self.left_frame, text="From:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.left_frame, text="To:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i
        ttk.Label(self.left_frame, text="Expense:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.left_frame, text="Income:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Label(self.right_frame, text="Remaining Credit:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.right_frame, text="Current Capital:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        date_start_frame = ttk.Frame(self.left_frame)
        date_start_frame.grid(row=self.i, column=1, sticky="ew", pady=10)
        datetime_entry(self.date_start, date_start_frame)
        date_end_frame = ttk.Frame(self.left_frame)
        date_end_frame.grid(row=self.i, column=1, sticky="ew", pady=10)
        datetime_entry(self.date_end, date_end_frame)
        ttk.Button(
            self.left_frame, text="Filter", style="Confirm.TButton", command=self.update_total
        ).grid(
            row=self.i, column=1, sticky="ew", ipady=10, padx=(20, 50)
        )
        ttk.Entry(self.left_frame, textvariable=self.total_expense, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.left_frame, textvariable=self.total_income, state="readonly").grid(row=self.i, column=1, sticky="ew")
        self.i = 0
        ttk.Entry(self.right_frame, textvariable=self.remaining_credit, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.right_frame, textvariable=self.current_capital, state="readonly").grid(row=self.i, column=1, sticky="ew")

    def update_total(self):
        start_year = self.date_start.year.get()
        start_month = self.date_start.month.get()
        start_day = self.date_start.day.get()
        end_year = self.date_end.year.get()
        end_month = self.date_end.month.get()
        end_day = self.date_end.day.get()
        if not (start_year or start_month or start_day or end_year or end_month or end_day):
            return None
        filter_date_start = date(start_year, start_month, start_day)
        filter_date_end = date(end_year, end_month, end_day)
        self.total_expense.set(summary.total_expense(filter_date_start, filter_date_end))
        self.total_income.set(summary.total_income(filter_date_start, filter_date_end))

    def refresh(self):
        current_time = date.today()
        self.date_start.year.set(current_time.year)
        self.date_start.month.set(current_time.month)
        self.date_start.day.set(current_time.day)
        self.date_end.year.set(current_time.year)
        self.date_end.month.set(current_time.month)
        self.date_end.day.set(current_time.day)
        self.total_expense.set(summary.total_expense())
        self.total_income.set(summary.total_income())
        self.remaining_credit.set(summary.remaining_credit())
        self.current_capital.set(summary.current_capital())
