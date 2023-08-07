from util import Util
from bhdate import BHDate
from bhtime import BHTime

import customtkinter as ctk
from PIL import Image
from datetime import datetime


class Task():
    def __init__(self, master, completed, title, date=None, time=None):
        BUTTON_WIDTH = BUTTON_HEIGHT = 24
        
        self.master = master
        self.date = date
        self.time = time
        
        int_var = ctk.IntVar(master, completed)
        string_var = ctk.StringVar(master, title)
        datetime_icon = Image.open(Util.resource_path('time.png'))
        remove_icon = Image.open(Util.resource_path('remove.png'))
        
        int_var.trace_add( 
            mode='write', 
            callback=lambda var, index, mode: master.write
        )
        string_var.trace_add(
            mode='write', 
            callback=lambda var, index, mode: master.write
        )
        
        self.checkbox = ctk.CTkCheckBox(
            master=master, 
            width=0, 
            text=None,
            variable=int_var,
            command=lambda task=self: master.move_task(task)
        )
        self.entry = ctk.CTkEntry(
            master=master, 
            textvariable=string_var,
            placeholder_text_color=('black', 'white')
        )
        self.datetime_button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(datetime_icon, datetime_icon, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=lambda task=self: master.time_task(task)
        )
        self.remove_button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(remove_icon, remove_icon, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=lambda task=self: master.remove_task(task)
        )
        
        self.datetime_label = None
        self.update_datetime_label()
            
        self.entry.bind(
            sequence='<Control-Key-a>',
            command=lambda event, widget=self.entry: Util.select_all(widget)
        )
        self.entry.bind(
            sequence='<Up>', 
            command=lambda event, task=self: master.navigate_to_prev(task)
        )
        self.entry.bind(
            sequence='<Down>', 
            command=lambda event, task=self: master.navigate_to_next(task)
        )
        self.entry.bind(
            sequence='<Button-1>',
            command=lambda event, canvas=master.master, widget=self.entry:
                        Util.scroll_into_view(canvas, widget)
        )
    
    def update_datetime_label(self):
        if self.date.is_set() and self.time.is_set():
            date_text = str(self.date)
            time_text = str(self.time)
            
            if self.datetime_label:
                self.datetime_label.configure(text=date_text + ' ' + time_text)
            else:
                self.datetime_label = ctk.CTkLabel(
                    master=self.master, 
                    text=date_text + ' ' + time_text,
                    fg_color=('white', '#4C4E52'),
                    corner_radius=6
                )
                
            if self.is_past():
                self.datetime_label.configure(text_color='red')
            else:
                self.datetime_label.configure(text_color=('gray14', 'gray84'))
    
    def destroy(self):
        self.checkbox.destroy()
        self.entry.destroy()
        self.datetime_button.destroy()
        self.remove_button.destroy()
        
        if self.datetime_label:
            self.datetime_label.destroy()
        
    def grid_forget(self):
        self.checkbox.grid_forget()
        self.entry.grid_forget()
        self.datetime_button.grid_forget()
        self.remove_button.grid_forget()
        
        if self.datetime_label:
            self.datetime_label.grid_forget()
    
    def serialize(self):
        return {
            'completed': self.checkbox.get(), 
            'title': self.entry.get(), 
            'date': str(self.date) if self.date and self.date.is_set() else None, 
            'time': str(self.time) if self.time and self.time.is_set() else None
        }
        
    def is_past(self):
        now = datetime.now()
        return now > datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute)
