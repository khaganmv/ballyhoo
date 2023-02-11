from util import Util
from task import Task

import customtkinter as ctk
import json
import platform


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
        self.master.configure(yscrollincrement=1)
        
        self.bind_mousewheel()

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
            self.ct = self.ct[:taskid] + self.ct[taskid + 1:]
        else:
            taskid = self.at.index(task)
            self.at = self.at[:taskid] + self.at[taskid + 1:]
            
        task.destroy()
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
            
            Util.scroll_into_view(self.master, ne)
            Util.shift_focus_from(self.ct[taskid].entry, ne)
        else:
            taskid = self.at.index(task)
            
            if taskid:
                Util.scroll_into_view(self.master, self.at[taskid - 1].entry)
                Util.shift_focus_from(self.at[taskid].entry, self.at[taskid - 1].entry)
            
    def navigate_to_next(self, task):
        if task.checkbox.get():
            taskid = self.ct.index(task)
            ne = self.next if taskid == len(self.ct) - 1 else self.ct[taskid + 1].entry
            
            if ne != self.next:
                Util.scroll_into_view(self.master, ne)
            
            Util.shift_focus_from(task.entry, ne)
        else:
            taskid = self.at.index(task)
            nif = self.ct[0].entry if self.sc and len(self.ct) else self.next
            ne = nif if taskid == len(self.at) - 1 else self.at[taskid + 1].entry
            
            if ne != self.next:
                Util.scroll_into_view(self.master, ne)
            
            Util.shift_focus_from(task.entry, ne)
            
    def bind_mousewheel(self):
        canvas = self.master
        system = platform.system()
        
        if system == 'Linux':
            canvas.bind_all(
                sequence='<Button-4>',
                func=lambda event:
                        canvas.yview_scroll(
                            -16 if int(canvas.canvasy(0)) - 16 >= 0 else 0,
                            'units'
                        )
            )
            
            canvas.bind_all(
                sequence='<Button-5>',
                func=lambda event: canvas.yview_scroll(16, 'units')
            )
        # elif system == 'Windows':
        #     canvas.bind_all(
        #         sequence='<MouseWheel>',
        #         func=lambda event: canvas.yview_scroll(-event.delta / 120, 'units')
        #     )
        # elif system == 'Darwin':
        #     canvas.bind_all(
        #         sequence='<MouseWheel>',
        #         func=lambda event: canvas.yview_scroll(-event.delta, 'units')
        #     )
