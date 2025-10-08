from tkinter import ttk, StringVar, messagebox
from db.orm import device
from datetime import datetime, timedelta
from template import Frame, DateClass, time_entry


class TimerFrame(Frame):
    def __init__(self, master):
        self.no_of_devices = device.get_all().count()
        self.device_range = range(self.no_of_devices)
        super().__init__(master)
        self.configure(style="G.TFrame", padding=1)
        self.update_devices()

    def tk_vars(self):
        self.names = [StringVar() for _ in self.device_range]
        self.dates = [DateClass() for _ in self.device_range]
        self.max_time = [StringVar() for _ in self.device_range]
        self.counter_type = [StringVar() for _ in self.device_range]
        self.counter = [StringVar() for _ in self.device_range]

    def main(self):
        timer_frame: list[ttk.Frame] = [None for _ in self.device_range]
        for i in self.device_range:
            timer_frame[i] = ttk.Frame(self)
            timer_frame[i].configure(style="G.TFrame", padding=1)
            timer_frame[i].place(relx=i / self.no_of_devices, rely=0, relheight=1.0, relwidth=1 / self.no_of_devices)
            ttk.Label(timer_frame[i], textvariable=self.names[i], anchor="center").place(relx=0, rely=0, relwidth=1.0, relheight=0.25)
            time_frame = ttk.Frame(timer_frame[i], padding=(20, 0))
            time_frame.place(relx=0, rely=0.25, relwidth=1.0, relheight=0.25)
            time_entry(self.dates[i], time_frame)
            button_frame = ttk.Frame(timer_frame[i], padding=(20, 0))
            button_frame.place(relx=0, rely=0.5, relwidth=1.0, relheight=0.25)
            ttk.Button(
                button_frame, text="Start / Stop", style="Confirm.TButton", command=lambda x=i: self.button(x)
            ).place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
            counter_frame = ttk.Frame(timer_frame[i])
            counter_frame.place(relx=0, rely=0.75, relwidth=1.0, relheight=0.25)
            ttk.Label(counter_frame, textvariable=self.counter_type[i], anchor="e").place(relx=0, rely=0, relwidth=0.4, relheight=1.0)
            ttk.Label(counter_frame, textvariable=self.counter[i], anchor="center").place(relx=0.4, rely=0, relwidth=0.6, relheight=1.0)

    def button(self, i: int):
        year = self.dates[i].year.get()
        month = self.dates[i].month.get()
        day = self.dates[i].day.get()
        hour = self.dates[i].hour.get() or 0
        minute = self.dates[i].minute.get() or 0
        max_time = self.max_time[i].get() or 0
        if not (year and month and day):
            messagebox.showwarning("Missing Values", "Values are Missing!")
            return None
        try:
            int(year)
            int(month)
            int(day)
            int(hour)
            int(minute)
            int(max_time)
        except ValueError:
            messagebox.showwarning("Wrong Type", "String used instead of numbers!")
            return None
        date = datetime(year, month, day, hour, minute)
        curr_device = self.devices[i]
        device.edit(curr_device.name, not curr_device.is_running, date, max_time)
        self.update_devices()

    def update_devices(self):
        self.devices = device.get_all()

    def refresh(self):
        current_time = datetime.now()
        for i, curr_device in enumerate(self.devices):
            self.names[i].set(curr_device.name)
            self.dates[i].year.set(current_time.year)
            self.dates[i].month.set(current_time.month)
            self.dates[i].day.set(current_time.day)
            self.dates[i].hour.set(current_time.hour)
            self.dates[i].minute.set(current_time.minute)
            self.max_time[i].set("")

    def refresh_time(self):
        current_time = datetime.now()
        for i, curr_device in enumerate(self.devices):
            if not curr_device.is_running:
                self.counter_type[i].set("")
                self.counter[i].set("")
                continue
            if curr_device.max_time:
                self.counter_type[i].set("<->:")
                final_time = curr_device.start_time + timedelta(minutes=curr_device.max_time)
                display_time: timedelta = final_time - current_time
            else:
                self.counter_type[i].set("<+>:")
                display_time: timedelta = current_time - curr_device.start_time
            total_seconds = int(max(display_time.total_seconds(), 0))
            timer = f"{total_seconds//3600}:{(total_seconds//60) % 60}:{total_seconds % 60}"
            self.counter[i].set(timer)
        self.after(1000, self.refresh_time)
