import tkinter as tk
from tkinter import ttk, StringVar, messagebox
from db.orm import expense
from datetime import datetime
from template import Frame, DateClass, datetime_entry
from variables import ROW_COUNT, FONT


class ExpenseFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)

    def tk_vars(self):
        self.table_columns = ("ID", "Name", "Cost", "Date")
        self.table_columns_width = (5, 300, 100, 100)
        self.table_columns_align = ("e", "w", "e", "e")
        self.name = StringVar()
        self.cost = StringVar()
        self.date = DateClass()
        self.id = StringVar()
        self.name_edit = StringVar()
        self.cost_edit = StringVar()

    def main(self):
        ttk.Label(self.add_frame, text="Name:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.add_frame, text="Cost:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.add_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Entry(self.add_frame, textvariable=self.name).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.add_frame, textvariable=self.cost).grid(row=self.i, column=1, sticky="ew")
        date_frame = ttk.Frame(self.add_frame)
        date_frame.grid(row=self.i, column=1, sticky="w")
        datetime_entry(self.date, date_frame)
        ttk.Button(
            self.add_frame, text="Add Expense", style="Confirm.TButton", command=self.save_expense
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

        self.list_table = ttk.Treeview(self.list_frame, show="headings", selectmode="browse", columns=self.table_columns, height=ROW_COUNT)
        for col_name, col_width, col_align in zip(self.table_columns, self.table_columns_width, self.table_columns_align):
            self.list_table.heading(col_name, text=col_name)
            self.list_table.column(col_name, width=col_width, anchor=col_align)
        self.list_table.place(relx=0, rely=0, relwidth=1.0, relheight=0.93)
        page_no_frame = ttk.Frame(self.list_frame)
        page_no_frame.place(relx=0, rely=0.93, relwidth=1.0, relheight=0.07)
        tk.Button(
            page_no_frame, text="<<", height=1, font=FONT, command=lambda: self.change_page(-1)
        ).place(relx=0, rely=0, relwidth=0.4, relheight=1.0)
        self.page_no_label = ttk.Label(page_no_frame, text="00/00", justify="center", font=FONT, anchor="center")
        self.page_no_label.place(relx=0.4, rely=0, relwidth=0.2, relheight=1.0)
        tk.Button(
            page_no_frame, text=">>", height=1, font=FONT, command=lambda: self.change_page(1)
        ).place(relx=0.6, rely=0, relwidth=0.4, relheight=1.0)

        self.i = 0
        ttk.Label(self.detail_frame, text="ID:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Name:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Cost:").grid(row=self.i, column=0, sticky="e", pady=10)
        ttk.Label(self.detail_frame, text="Date:").grid(row=self.i, column=0, sticky="e", pady=10)
        self.i = 0
        ttk.Entry(self.detail_frame, textvariable=self.id, state="readonly").grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.name_edit).grid(row=self.i, column=1, sticky="ew")
        ttk.Entry(self.detail_frame, textvariable=self.cost_edit).grid(row=self.i, column=1, sticky="ew")
        date_frame_edit = ttk.Frame(self.detail_frame)
        date_frame_edit.grid(row=self.i, column=1, sticky="w")
        datetime_entry(self.date, date_frame_edit)
        ttk.Button(
            self.detail_frame, text="Update Expense", style="Confirm.TButton", command=self.update_expense
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )
        ttk.Button(
            self.detail_frame, text="Delete Expense", style="Delete.TButton", command=self.delete_expense
        ).grid(
            row=self.i, column=0, columnspan=2, sticky="ew", ipady=10
        )

    def events(self):
        self.list_table.bind("<Double-Button-1>", self.select_expense)

    def save_expense(self):
        name = self.name.get()
        cost = self.cost.get()
        year = self.date.year.get()
        month = self.date.month.get()
        day = self.date.day.get()
        hour = self.date.hour.get() or 0
        minute = self.date.minute.get() or 0
        if not (name and cost and year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(cost)
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        date = datetime(year, month, day, hour, minute)
        expense.create(name, cost, date)
        self.refresh()

    def update_expense(self):
        id = self.id.get()
        name = self.name.get()
        cost = self.cost.get()
        year = self.date.year.get()
        month = self.date.month.get()
        day = self.date.day.get()
        hour = self.date.hour.get() or 0
        minute = self.date.minute.get() or 0
        if not (id and name and cost and year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            float(cost)
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        date = datetime(year, month, day, hour, minute)
        expense.edit(id, name, cost, date)
        self.refresh()

    def delete_expense(self):
        expense_id = self.id.get()
        if not expense_id:
            return None
        confirmation = messagebox.askyesno("Are you sure?", f"Do you want to delete expense of ID.{expense_id}?")
        if not confirmation:
            return None
        expense.del_res(expense_id)
        self.refresh()

    def select_expense(self, *args):
        selected_expense = self.list_table.selection()
        if not selected_expense:
            return None
        expense_id = self.list_table.item(selected_expense[0]).get("values", [None])[0]
        e = expense.get_by_id(expense_id)
        self.id.set(e.id)
        self.name_edit.set(e.name)
        self.cost_edit.set(e.cost)
        self.date.year.set(e.date.year)
        self.date.month.set(e.date.month)
        self.date.day.set(e.date.day)
        self.date.hour.set(e.date.hour)
        self.date.minute.set(e.date.minute)
        self.detail_frame.tkraise()

    def update_table(self):
        expenses, expense_count = expense.get_paginated(self.page_no)
        self.total_pages = (expense_count - 1) // ROW_COUNT + 1
        self.page_no_label.config(text=f"{self.page_no}/{self.total_pages}")
        self.list_table.delete(*self.list_table.get_children())
        for row in expenses:
            self.list_table.insert('', tk.END, values=(row.id, row.name, row.cost, row.date))

    def refresh(self):
        self.add_frame.tkraise()
        self.name.set("")
        self.cost.set("")

        self.name_edit.set("")
        self.cost_edit.set("")

        current_time = datetime.now()
        self.date.year.set(current_time.year)
        self.date.month.set(current_time.month)
        self.date.day.set(current_time.day)
        self.date.hour.set(current_time.hour)
        self.date.minute.set(current_time.minute)

        self.page_no = 1
        self.update_table()
