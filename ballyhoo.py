import tkinter as tk
import customtkinter as ctk


class Task():
    def __init__(self, checkbox, entry):
        self.checkbox = checkbox
        self.entry = entry


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tasks = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
    def add_item(self, text):
        # configure checkbox
        checkbox = ctk.CTkCheckBox(
            master=self, 
            width=0, 
            text=None
        )
        checkbox.grid(row=len(self.tasks), column=0)
        
        # configure entry
        entry = ctk.CTkEntry(
            master=self, 
            placeholder_text=text,
            placeholder_text_color=('black', 'white')
        )
        entry.grid(
            row=len(self.tasks), 
            column=1, 
            padx=(4, 8), 
            pady=(4, 0), 
            sticky='ew'
        )
        
        self.tasks.append(Task(checkbox=checkbox, entry=entry))


class Ballyhoo(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode('system')
        ctk.set_default_color_theme('dark-blue')

        self.title("Ballyhoo")
        self.geometry("500x400")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        
        # configure show completed switch
        self.scs = ctk.CTkSwitch(master=self, text='Show Completed')    
        self.scs.grid(row=0, column=0, padx=10, pady=10)
        
        # configure dark mode switch
        self.dms = ctk.CTkSwitch(
            master=self, 
            text='Dark Mode', 
            command=self.toggle_dark_mode
        )
        if ctk.get_appearance_mode() == 'Dark':
            self.dms.select()
        self.dms.grid(row=0, column=1, padx=10, pady=10)
        
        # configure task list
        self.tl = ScrollableFrame(master=self)
        self.tl.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        
        # configure user input field
        self.uif = ctk.CTkEntry(master=self)
        self.uif.bind(sequence='<Return>', command=self.add_item)
        self.uif.bind(sequence='<Control-Key-a>', command=self.select_all)
        self.uif.grid(
            row=2, 
            column=0, 
            columnspan=2, 
            padx=25, 
            pady=(10, 20), 
            sticky='ew'
        )
        
    def toggle_dark_mode(self):
        ctk.set_appearance_mode(
            'dark' if ctk.get_appearance_mode() == 'Light' else 'light'
        )
    
    def add_item(self, master):
        text = self.uif.get()
        if text:
            self.tl.add_item(text)
            self.uif.delete(0, tk.END)

    def select_all(self, master):
        self.uif.select_range(0, tk.END)
        self.uif.icursor(tk.END)
        return 'break'