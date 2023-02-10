from util import Util
from settings import Settings

import customtkinter as ctk
import json
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
        
        # configure button
        im_width = im_height = 24
        im = Image.open('resources/remove.png')
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
        

class TaskList(ctk.CTkScrollableFrame):
    def __init__(self, master, sc, **kwargs):
        super().__init__(master, **kwargs)
        
        tasks = self.read_tasks()
        
        # active tasks
        self.at = list(filter(lambda task: not task.checkbox.get(), tasks))
        # completed tasks
        self.ct = list(filter(lambda task: task.checkbox.get(), tasks))
        # show completed
        self.sc = sc
        # next widget
        self.next = None
        
        # configure yscrollincrement for scrolling
        self._parent_canvas.configure(yscrollincrement=1)
        
        self.grid_rowconfigure(0, weight=1)
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
        json.dump([task.serialize() for task in self.at + self.ct], tf)
        tf.close()
    
    def add_task(self, text):        
        task = Task(self, completed=False, title=text)
        self.add_to_task_list(task, len(self.at))
        self.at.append(task)
        if self.sc and len(self.ct):
            self.update_task_list()
        self.write_tasks()
    
    def move_task(self, task):
        if task.checkbox.get():
            taskid = self.at.index(task)
            self.at = self.at[:taskid] + self.at[taskid + 1:]
            self.ct.append(task)
        else:
            taskid = self.ct.index(task)
            self.ct = self.ct[:taskid] + self.ct[taskid + 1:]
            self.at.append(task)
            
        self.update_task_list()
        self.write_tasks()
    
    def remove_task(self, task):
        if task.checkbox.get():
            taskid = self.ct.index(task)
            task.destroy()
            self.ct = self.ct[:taskid] + self.ct[taskid + 1:]
        else:
            taskid = self.at.index(task)
            task.destroy()
            self.at = self.at[:taskid] + self.at[taskid + 1:]
            
        self.update_task_list()
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
        
        task.button.grid(row=rowid, column=2)
    
    def update_task_list(self):
        for i, task in enumerate(self.at):
            self.add_to_task_list(task, i)
            
        for i, task in enumerate(self.ct):
            if self.sc:
                self.add_to_task_list(task, i + len(self.at))
            else:
                task.grid_forget()
        
    def navigate_to_prev(self, task):
        if task.checkbox.get():
            taskid = self.ct.index(task)
            ne = self.ct[taskid - 1].entry if taskid else self.at[-1].entry
            
            Util.scroll_into_view(self._parent_canvas, ne)
            Util.shift_focus_from(self.ct[taskid].entry, ne)
        else:
            taskid = self.at.index(task)
            
            if taskid:
                Util.scroll_into_view(self._parent_canvas, self.at[taskid - 1].entry)
                Util.shift_focus_from(self.at[taskid].entry, self.at[taskid - 1].entry)
            
    def navigate_to_next(self, task):
        if task.checkbox.get():
            taskid = self.ct.index(task)
            ne = self.next if taskid == len(self.ct) - 1 else self.ct[taskid + 1].entry
            
            if ne != self.next:
                Util.scroll_into_view(self._parent_canvas, ne)
            
            Util.shift_focus_from(task.entry, ne)
        else:
            taskid = self.at.index(task)
            nif = self.ct[0].entry if self.sc and len(self.ct) else self.next
            ne = nif if taskid == len(self.at) - 1 else self.at[taskid + 1].entry
            
            if ne != self.next:
                Util.scroll_into_view(self._parent_canvas, ne)
            
            Util.shift_focus_from(task.entry, ne)
       
        
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
        
        Util.scroll_into_view(self.tl._parent_canvas, ne)
        Util.shift_focus_from(self.uif, ne)