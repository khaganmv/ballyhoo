from util import Util

import customtkinter as ctk
from PIL import Image


class Task():
    def __init__(self, master, completed, title):
        self.master = master
        
        # configure checkbox
        iv = ctk.IntVar(master, completed)
        iv.trace_add('write', master.write_tasks)
        self.checkbox = ctk.CTkCheckBox(
            master=master, 
            width=0, 
            text=None,
            variable=iv,
            command=lambda task=self: self.master.move_task(task)
        )
        
        # configure entry
        sv = ctk.StringVar(master, title)
        sv.trace_add('write', master.write_tasks)
        self.entry = ctk.CTkEntry(
            master=master, 
            textvariable=sv,
            placeholder_text_color=('black', 'white')
        )
        self.entry.bind(
            sequence='<Control-Key-a>',
            command=lambda event, widget=self.entry: Util.select_all(widget)
        )
        self.entry.bind(
            sequence='<Up>', 
            command=lambda event, widget=self: self.master.navigate_to_prev(widget)
        )
        self.entry.bind(
            sequence='<Down>', 
            command=lambda event, widget=self: self.master.navigate_to_next(widget)
        )
        self.entry.bind(
            sequence='<Button-1>',
            command=lambda event, canvas=self.master.master, widget=self.entry:
                        Util.scroll_into_view(canvas, widget)
        )
        
        # configure button
        im_width = im_height = 24
        im = Image.open(Util.resource_path('remove.png'))
        self.button = ctk.CTkButton(
            master=master,
            width=im_width,
            height=im_height,
            fg_color='transparent',
            text=None,
            image=ctk.CTkImage(im, im, size=(im_width, im_height)),
            command=lambda task=self: master.remove_task(self)
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
