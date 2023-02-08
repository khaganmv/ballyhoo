import tkinter as tk
import customtkinter as ctk
import json


class Task():
    def __init__(self, master, completed, title):
        iv = ctk.IntVar(master, completed)
        iv.trace_add('write', master.write_tasks)
        self.checkbox = ctk.CTkCheckBox(
            master=master, 
            width=0, 
            text=None,
            variable=iv
        )
        
        sv = ctk.StringVar(master, title)
        sv.trace_add('write', master.write_tasks)
        self.entry = ctk.CTkEntry(
            master=master, 
            textvariable=sv,
            placeholder_text_color=('black', 'white')
        )
        
    def serialize(self):
        return { 'completed': self.checkbox.get(), 'title': self.entry.get() }
        

class TaskList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tasks = self.read_tasks()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        
        self.update_task_list()

    def read_tasks(self):
        tasks = []
        
        tf = open('tasks.json', 'a+')
        if tf.tell():
            tf.seek(0)
            data = json.load(tf)
            tasks = [Task(self, task['completed'], task['title']) for task in data]
        tf.close()
        
        return tasks
    
    def write_tasks(self, *args):
        tf = open('tasks.json', 'w')
        json.dump([task.serialize() for task in self.tasks], tf)
        tf.close()
    
    def add_task(self, text):        
        task = Task(self, completed=False, title=text)
        self.add_to_task_list(task, len(self.tasks))
        self.tasks.append(task)
        self.write_tasks()
    
    def add_to_task_list(self, task, rowid):
        task.checkbox.grid(row=rowid, column=0)
        
        task.entry.grid(
            row=rowid, 
            column=1, 
            padx=(4, 8), 
            pady=(4, 0), 
            sticky='ew'
        )
    
    def update_task_list(self):
        for i, task in enumerate(self.tasks):
            self.add_to_task_list(task, i)
        

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
        self.tl = TaskList(master=self)
        self.tl.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        
        # configure user input field
        self.uif = ctk.CTkEntry(master=self)
        self.uif.bind(sequence='<Return>', command=self.add_task)
        self.uif.bind(sequence='<Control-Key-a>', command=self.select_all)
        self.uif.grid(
            row=2, 
            column=0, 
            columnspan=2, 
            padx=25, 
            pady=(10, 20), 
            sticky='ew'
        )
        
        self.uif.focus()
        
    def toggle_dark_mode(self):
        ctk.set_appearance_mode(
            'dark' if ctk.get_appearance_mode() == 'Light' else 'light'
        )
    
    def add_task(self, master):
        text = self.uif.get()
        if text:
            self.tl.add_task(text)
            self.uif.delete(0, tk.END)

    def select_all(self, master):
        self.uif.select_range(0, tk.END)
        self.uif.icursor(tk.END)
        return 'break'