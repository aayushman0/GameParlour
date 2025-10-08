import tkinter as tk
from tkinter import ttk, IntVar


class Frame(ttk.Frame):
    def __init__(self, master: tk.Tk | ttk.Frame):
        super().__init__(master)
        self._i: int = 0
        self.page_no: int = 1
        self.total_pages: int = 1
        self.prev_frame: ttk.Frame = None
        self.tk_vars()
        self.add_frame = ttk.Frame(self, padding=5)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)
        self.detail_frame = ttk.Frame(self, padding=5)
        self.detail_frame.columnconfigure(1, weight=1)
        self.detail_frame.place(relx=0, rely=0, relwidth=0.3, relheight=1.0)
        self.list_frame = ttk.Frame(self, padding=5)
        self.list_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1.0)
        self.main()
        self.events()
        self.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    @property
    def i(self) -> int:
        self._i += 1
        return self._i - 1

    @i.setter
    def i(self, x) -> None:
        self._i = x

    def tk_vars(self) -> None:
        pass

    def main(self) -> None:
        pass

    def update_table(self) -> None:
        pass

    def events(self) -> None:
        pass

    def refresh(self) -> None:
        pass

    def set_active(self) -> None:
        self.tkraise()
        self.refresh()

    def change_page(self, i: int):
        next_page_no = self.page_no + i
        if next_page_no in range(1, self.total_pages + 1):
            self.page_no = next_page_no
            self.update_table()


class DateClass:
    def __init__(self):
        self.year = IntVar()
        self.month = IntVar()
        self.day = IntVar()
        self.hour = IntVar()
        self.minute = IntVar()


def datetime_entry(cls: DateClass, frame: ttk.Frame):
    frame.columnconfigure((0, 2, 4, 6, 8), weight=1)
    ttk.Spinbox(frame, textvariable=cls.year, from_=2000, to=2999, justify="right", width=22).grid(row=0, column=0, sticky="ew")
    ttk.Label(frame, text="/").grid(row=0, column=1)
    ttk.Spinbox(frame, textvariable=cls.month, from_=1, to=12, justify="center").grid(row=0, column=2)
    ttk.Label(frame, text="/").grid(row=0, column=3)
    ttk.Spinbox(frame, textvariable=cls.day, from_=1, to=32).grid(row=0, column=4)
    ttk.Label(frame, text="  ").grid(row=0, column=5)
    ttk.Spinbox(frame, textvariable=cls.hour, from_=0, to=23, justify="right").grid(row=0, column=6)
    ttk.Label(frame, text=":").grid(row=0, column=7)
    ttk.Spinbox(frame, textvariable=cls.minute, from_=0, to=59).grid(row=0, column=8)


def time_entry(cls: DateClass, frame: tk.Frame):
    frame.columnconfigure((0, 2), weight=1)
    ttk.Spinbox(frame, textvariable=cls.hour, from_=0, to=23, justify="right").grid(row=0, column=0)
    ttk.Label(frame, text=":").grid(row=0, column=1)
    ttk.Spinbox(frame, textvariable=cls.minute, from_=0, to=59).grid(row=0, column=2)


def number_seperator(num: float | int) -> str:
    num = float(num)
    string_int, string_dec = str(num).split(".")
    full_string = string_int[-3:]
    if len(string_int) > 3:
        full_string = string_int[-3:]
        for i in range((len(string_int[:-3])+1)//2):
            full_string = string_int[-(3+2*(i+1)):-(3+2*i)] + "," + full_string
    return full_string + "." + string_dec
