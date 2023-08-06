from util import Util

import customtkinter as ctk
from PIL import Image
from datetime import datetime


class Task():
    def __init__(self, master, completed, title, date=None, time=None):
        BUTTON_WIDTH = BUTTON_HEIGHT = 24
        
        self.date = date
        self.time = time
        
        int_var = ctk.IntVar(master, completed)
        string_var = ctk.StringVar(master, title)
        edit, remove = Image.open('resources/edit.png'), Image.open('resources/remove.png')
        # edit, remove = Image.open(Util.resource_path('resources/edit.png')), Image.open(Util.resource_path('resources/remove.png'))
        
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
        
        self.edit_button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(edit, edit, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=lambda task=self: master.edit_task(task)
        )
        
        self.remove_button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(remove, remove, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=lambda task=self: master.remove_task(task)
        )
        
        self.date_label = self.time_label = None
        
        if self.date and self.date.is_set():
            date_text = str(self.date)
            self.date_label = ctk.CTkLabel(master=master, text=date_text)
            
        if self.time and self.time.is_set():
            time_text = str(self.time)
            self.time_label = ctk.CTkLabel(master=master, text=time_text)
            
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
        
    def destroy(self):
        self.checkbox.destroy()
        self.entry.destroy()
        self.edit_button.destroy()
        self.remove_button.destroy()
        
        if self.date_label:
            self.date_label.destroy()
            
        if self.time_label:
            self.time_label.destroy()
        
    def grid_forget(self):
        self.checkbox.grid_forget()
        self.entry.grid_forget()
        self.button.grid_forget()
        
        if self.date_label:
            self.date_label.grid_forget()
            
        if self.time_label:
            self.time_label.grid_forget()
    
    def serialize(self):
        return {
            'completed': self.checkbox.get(), 
            'title': self.entry.get(), 
            'date': str(self.date) if self.date and self.date.is_set() else None, 
            'time': str(self.time) if self.time and self.time.is_set() else None
        }
        
    def is_past(self):
        now = datetime.now()
        
        if self.date and self.date.is_set() and self.date.is_past(now):
            return True
        elif self.time and self.time.is_set() and self.time.is_past(now):
            return True
            
        return False
