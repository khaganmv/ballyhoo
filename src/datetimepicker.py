from bhcalendar import BHCalendar
from bhtimepicker import BHTimePicker

import customtkinter as ctk
from datetime import datetime


class DateTimePicker(ctk.CTkToplevel):
    def __init__(self, master, date, time, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title('DateTime Picker')
        self.geometry('500x400')
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.datetime = datetime.now()
        
        self.datetime_tabview = ctk.CTkTabview(master=self)
        self.date_tab = self.datetime_tabview.add('Date')
        self.time_tab = self.datetime_tabview.add('Time')
        
        self.date_tab.rowconfigure(0, weight=1)
        self.date_tab.columnconfigure(0, weight=1)
        self.time_tab.rowconfigure(0, weight=1)
        self.time_tab.columnconfigure(0, weight=1)
        
        self.date_picker = BHCalendar(
            master=self.date_tab, 
            datetime=self.datetime,
            date=date, 
            fg_color='transparent'
        )
        self.time_picker = BHTimePicker(
            master=self.time_tab, 
            datetime=self.datetime,
            date=date, 
            time=time
        )
        
        self.datetime_tabview.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
        self.date_picker.grid(row=0, column=0, padx=20, pady=(5, 0), sticky='nsew')
        self.time_picker.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')
