from bhcalendar import BHCalendar
from bhtimepicker import BHTimePicker

import customtkinter as ctk
from datetime import datetime


class DateTimePicker(ctk.CTkToplevel):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title('DateTime Picker')
        self.geometry('500x400')
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.task = task
        self.datetime = datetime.now()
        
        self.datetime_tabview = ctk.CTkTabview(master=self)
        self.date_tab = self.datetime_tabview.add('Date')
        self.time_tab = self.datetime_tabview.add('Time')
        
        self.date_tab.rowconfigure(0, weight=1)
        self.date_tab.columnconfigure(0, weight=1)
        self.time_tab.rowconfigure(0, weight=1)
        self.time_tab.columnconfigure(0, weight=1)
        self.save_button = ctk.CTkButton(master=self, text='Save', command=self.save_datetime)
        
        self.date_picker = BHCalendar(
            master=self.date_tab, 
            datetime=self.datetime,
            task=task,
            fg_color='transparent'
        )
        self.time_picker = BHTimePicker(
            master=self.time_tab, 
            datetime=self.datetime,
            task=task,
            fg_color='transparent'
        )
        
        self.datetime_tabview.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        self.date_picker.grid(row=0, column=0, padx=20, pady=(5, 0), sticky='nsew')
        self.time_picker.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        self.save_button.grid(row=1, column=0, padx=20, pady=(0, 20), sticky='ns')
    
    def save_datetime(self):
        self.task.date.set_date(self.date_picker.day, self.date_picker.month, self.date_picker.year)
        self.task.time.set_time(self.time_picker.hour, self.time_picker.minute)
        self.task.update_datetime_label()
        self.task.master.update_task_list()
        self.task.master.write()
        self.destroy()
