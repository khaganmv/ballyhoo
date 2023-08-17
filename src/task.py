from util import Util
from bhdate import BHDate
from bhtime import BHTime

import customtkinter as ctk
from PIL import Image
from datetime import datetime
import tkinter as tk


class Task():
    def __init__(self, master, completed, title, date, time):
        BUTTON_WIDTH = BUTTON_HEIGHT = 24
        
        self.master = master
        self.date = date
        self.time = time
        self.font = ctk.CTkFont('fixedsys', 12)
        self.lines = 1
        
        int_var = ctk.IntVar(master, completed)
        datetime_icon_light = Image.open(Util.resource_path('clock_light.png'))
        datetime_icon_dark = Image.open(Util.resource_path('clock_dark.png'))
        remove_icon = Image.open(Util.resource_path('remove.png'))
        
        int_var.trace_add( 
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
        self.textbox = ctk.CTkTextbox(
            master=master, 
            font=self.font,
            height=24,
            activate_scrollbars=False
        )
        self.textbox.insert(ctk.INSERT, title)
        self.datetime_button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(datetime_icon_light, datetime_icon_dark, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
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
            
        self.textbox.bind(
            sequence='<Control-Key-a>',
            command=lambda event, widget=self.textbox: Util.select_all(widget)
        )
        self.textbox.bind(
            sequence='<Up>', 
            command=lambda event, task=self: master.navigate_to_prev(task)
        )
        self.textbox.bind(
            sequence='<Down>', 
            command=lambda event, task=self: master.navigate_to_next(task)
        )
        self.textbox.bind(
            sequence='<Button-1>',
            command=lambda event, canvas=master.master, widget=self.textbox: Util.scroll_into_view(canvas, widget)
        )
        self.textbox.bind(
            sequence='<KeyRelease>',
            command=lambda event: self.write()
        )
    
    def write(self):
        if self.textbox.edit_modified():
            self.master.write()
            self.textbox.edit_modified(False)
    
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
                    corner_radius=6,
                    font=self.font
                )
                
            if self.is_past():
                self.datetime_label.configure(text_color='red')
            else:
                self.datetime_label.configure(text_color=('gray14', 'gray84'))
    
    def resize(self):
        lines = int(1 / (self.textbox.yview()[1] - self.textbox.yview()[0]))
        
        if lines != self.lines:
            row = self.textbox.grid_info()['row']
            self.lines = lines
            self.textbox.configure(height=24 * lines)
            self.textbox.grid(row=row, column=1, padx=(4, 8), pady=2, sticky='ew')
        
    def destroy(self):
        self.checkbox.destroy()
        self.textbox.destroy()
        self.datetime_button.destroy()
        self.remove_button.destroy()
        
        if self.datetime_label:
            self.datetime_label.destroy()
        
    def grid_forget(self):
        self.checkbox.grid_forget()
        self.textbox.grid_forget()
        self.datetime_button.grid_forget()
        self.remove_button.grid_forget()
        
        if self.datetime_label:
            self.datetime_label.grid_forget()
    
    def serialize(self):
        return {
            'completed': self.checkbox.get(), 
            'title': self.textbox.get('1.0', 'end-1c'), 
            'date': str(self.date) if self.date and self.date.is_set() else None, 
            'time': str(self.time) if self.time and self.time.is_set() else None
        }
        
    def is_past(self):
        now = datetime.now()
        return now > datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute)
