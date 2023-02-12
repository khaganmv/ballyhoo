from util import Util

import customtkinter as ctk
from PIL import Image


class Task():
    def __init__(self, master, completed, title):
        BUTTON_WIDTH = BUTTON_HEIGHT = 24
        
        int_var = ctk.IntVar(master, completed)
        string_var = ctk.StringVar(master, title)
        image = Image.open('resources/remove.png')
        # image = Image.open(Util.resource_path('remove.png'))
        
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
        
        self.button = ctk.CTkButton(
            master=master,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(image, image, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=lambda task=self: master.remove_task(task)
        )
        
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
        self.button.destroy()
        
    def grid_forget(self):
        self.checkbox.grid_forget()
        self.entry.grid_forget()
        self.button.grid_forget()
    
    def serialize(self):
        return { 'completed': self.checkbox.get(), 'title': self.entry.get() }
