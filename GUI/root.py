import tkinter as tk
from tkinter import ttk
from GUI import device, expense, income, credit, summary, timer
from variables import APP_NAME, FONT, FONT_SMALL


root = tk.Tk()
root.title(APP_NAME)
root.state("zoomed")
root.minsize(960, 540)
root.option_add("*Font", FONT)

# -------------------------------------------------- Style -------------------------------------------------- #
style = ttk.Style(root)
style.theme_use("alt")
style.configure("B.TFrame", background="Black")
style.configure("G.TFrame", background="Gray")
style.configure("Confirm.TButton", background="#44dd55", font=FONT)
style.configure("Delete.TButton", background="#dd4455", font=FONT)
style.configure("Back.TButton", background="#f0f0f0", font=FONT)
style.configure("Treeview", font=FONT)
style.configure("Treeview.Heading", font=FONT)
style.map("TEntry", foreground=[("disabled", 'black')])
# ----------------------------------------------------------------------------------------------------------- #

top_frame = ttk.Frame(root)
top_frame.place(relx=0, rely=0, relwidth=1.0, relheight=0.2)
main_frame = ttk.Frame(root)
main_frame.place(relx=0, rely=0.2, relwidth=1.0, relheight=0.8)

# -------------------------------------------------- Pages -------------------------------------------------- #
timer_frame = timer.TimerFrame(top_frame)
device_frame = device.DeviceFrame(main_frame)
expense_frame = expense.ExpenseFrame(main_frame)
income_frame = income.IncomeFrame(main_frame)
credit_frame = credit.CreditFrame(main_frame)
summary_frame = summary.SummaryFrame(main_frame)
income_frame.set_active()
timer_frame.refresh()
timer_frame.refresh_time()
# ----------------------------------------------------------------------------------------------------------- #

# ------------------------------------------------- MenuBar ------------------------------------------------- #
menubar = tk.Menu(root, tearoff=False)
menubar.add_command(label="Summary", command=summary_frame.set_active, font=FONT_SMALL)
menubar.add_command(label="Income", command=income_frame.set_active, font=FONT_SMALL)
menubar.add_command(label="Expense", command=expense_frame.set_active, font=FONT_SMALL)
menubar.add_command(label="Credit", command=credit_frame.set_active, font=FONT_SMALL)
menubar.add_command(label="Devices", command=device_frame.set_active, font=FONT_SMALL)
menubar.add_command(label="Refresh", command=timer_frame.refresh, font=FONT_SMALL)
root.config(menu=menubar)
# ----------------------------------------------------------------------------------------------------------- #


def start():
    root.mainloop()
