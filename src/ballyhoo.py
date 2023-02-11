from util import Util
from settings import Settings
from tasklist import TaskList

import customtkinter as ctk

        
class Ballyhoo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = Settings()

        ctk.set_appearance_mode(self.settings.am)
        ctk.set_default_color_theme('dark-blue')

        self.title("Ballyhoo")
        self.geometry("500x400")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        # configure show completed switch
        self.scs = ctk.CTkSwitch(master=self, text='Show Completed')
        if self.settings.sc:
            self.scs.select()
        self.scs.grid(row=0, column=0, padx=10, pady=10)
        
        # configure dark mode switch
        self.dms = ctk.CTkSwitch(master=self, text='Dark Mode', command=self.toggle_dark_mode)
        if ctk.get_appearance_mode() == 'Dark':
            self.dms.select()
        self.dms.grid(row=0, column=1, padx=10, pady=10)
        
        # configure task list
        self.tl = TaskList(master=self, sc=self.settings.sc)
        self.tl.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        
        # configure user input field
        self.uif = ctk.CTkEntry(master=self)
        self.uif.bind(sequence='<Return>', command=self.add_task)
        self.uif.bind(
            sequence='<Control-Key-a>', 
            command=lambda event, widget=self.uif: Util.select_all(widget)
        )
        self.uif.bind(sequence='<Up>', command=self.navigate_to_prev)
        self.uif.grid(row=2, column=0, columnspan=2, padx=25, pady=(10, 20), sticky='ew')
        
        self.scs.configure(command=self.show_completed)
        
        # store reference to uif in tl for navigation
        self.tl.next = self.uif
        
        self.uif.focus()
        
    def show_completed(self):
        self.settings.sc = self.tl.sc = self.scs.get()
        self.tl.update_task_list()
        self.settings.write_settings()
        
    def toggle_dark_mode(self):
        self.settings.am = am = 'dark' if ctk.get_appearance_mode() == 'Light' else 'light'
        ctk.set_appearance_mode(am)
        self.settings.write_settings()
        
    def add_task(self, event):
        text = self.uif.get()
        if text:
            self.tl.add_task(text)
            self.uif.delete(0, ctk.END)
    
    def navigate_to_prev(self, event):
        ne = self.tl.ct[-1].entry if self.tl.sc and len(self.tl.ct) else self.tl.at[-1].entry
        
        Util.scroll_into_view(self.tl.master, ne)
        Util.shift_focus_from(self.uif, ne)
