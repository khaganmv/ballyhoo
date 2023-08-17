from util import Util
from task import Task
from bhdate import BHDate
from bhtime import BHTime
from datetimepicker import DateTimePicker

import customtkinter as ctk
import json
import platform


class TaskList(ctk.CTkScrollableFrame):
    def __init__(self, master, dir, input_field, **kwargs):
        super().__init__(master, **kwargs)
        self.dir = dir
        self.input_field = input_field
        
        tasks = self.read()
        
        self.active_tasks = list(filter(lambda task: not task.checkbox.get(), tasks))
        self.completed_tasks = list(filter(lambda task: task.checkbox.get(), tasks))
        self.show_completed = master.settings.show_completed
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.bind_mousewheel()
        self.update_task_list()

    def read(self):
        tasks = []
        
        with open(self.dir + 'tasks.json', 'a+') as tasks_file:
            if tasks_file.tell():
                tasks_file.seek(0)
                data = json.load(tasks_file)
                tasks = [
                    Task(
                        self, 
                        task['completed'], 
                        task['title'],
                        BHDate.from_str(task['date']) if task['date'] else BHDate(),
                        BHTime.from_str(task['time']) if task['time'] else BHTime()
                    ) 
                    for task in data]
                
            tasks_file.close()
        
        return tasks
    
    def write(self):
        with open(self.dir + 'tasks.json', 'w') as tasks_file:
            json.dump(
                [task.serialize() for task in self.active_tasks + self.completed_tasks], 
                tasks_file,
                indent=4
            )
            tasks_file.close()
    
    def add_task(self, title):
        task = Task(self, completed=False, title=title, date=BHDate(), time=BHTime())
        
        self.add_to_task_list(task, len(self.active_tasks))
        self.active_tasks.append(task)
        
        if self.show_completed and len(self.completed_tasks):
            self.update_task_list()
            
        self.update_idletasks()
        Util.scroll_into_view(self.master, task.textbox)
        self.write()
    
    def move_task(self, task):
        if task.checkbox.get():
            self.active_tasks.remove(task)
            self.completed_tasks.append(task)
        else:
            self.completed_tasks.remove(task)
            self.active_tasks.append(task)
            
        self.update_task_list()
        self.write()
    
    def time_task(self, task):
        datetime_picker = DateTimePicker(master=self, task=task)
        datetime_picker.lift()
        datetime_picker.focus()
    
    def remove_task(self, task):
        if task.checkbox.get():
            self.completed_tasks.remove(task)
        else:
            self.active_tasks.remove(task)
            
        task.grid_forget()
        task.destroy()
        self.update_task_list()
        self.write()
    
    def add_to_task_list(self, task, rowid):
        task.checkbox.grid(row=rowid, column=0, pady=2)
        task.textbox.grid(row=rowid, column=1, padx=(4, 8), pady=2, sticky='ew')
        task.datetime_button.grid(row=rowid, column=3, pady=2)
        task.remove_button.grid(row=rowid, column=4, pady=2)
        
        if task.datetime_label:
            task.datetime_label.grid(row=rowid, column=2, padx=4, pady=2)
            
    def update_task_list(self):
        self.update()
        
        for i, task in enumerate(self.active_tasks):
            self.add_to_task_list(task, i)
            
        for i, task in enumerate(self.completed_tasks):
            if self.show_completed:
                self.add_to_task_list(task, i + len(self.active_tasks))
            else:
                task.grid_forget() 
    
    def resize_textboxes(self):
        tasks = self.active_tasks
        
        if self.show_completed:
            tasks += self.completed_tasks
        
        self.update()
            
        for task in tasks:
            task.resize()
    
    def update_datetime_labels(self):
        tasks = self.active_tasks + self.completed_tasks if self.show_completed else self.active_tasks
        
        for task in tasks:
            if task.datetime_label:
                if task.is_past():
                    task.datetime_label.configure(text_color='red')
    
    def navigate_to_prev(self, task):
        prev_entry = None
        
        if task.checkbox.get():
            completed_index = self.completed_tasks.index(task)
            
            if completed_index:
                prev_entry = self.completed_tasks[completed_index - 1].textbox
            elif len(self.active_tasks):
                prev_entry = self.active_tasks[-1].textbox
            
            if prev_entry:
                Util.scroll_into_view(self.master, prev_entry)
                Util.shift_focus_from(task.textbox, prev_entry)
        else:
            active_index = self.active_tasks.index(task)
            
            if active_index:
                prev_entry = self.active_tasks[active_index - 1].textbox
                
                Util.scroll_into_view(self.master, prev_entry)
                Util.shift_focus_from(task.textbox, prev_entry)
            
    def navigate_to_next(self, task):
        if task.checkbox.get():
            if task == self.completed_tasks[-1]:
                next_entry = self.input_field
            else:
                completed_index = self.completed_tasks.index(task)
                next_entry = self.completed_tasks[completed_index + 1].textbox
                
                Util.scroll_into_view(self.master, next_entry)
                
            Util.shift_focus_from(task.textbox, next_entry)
        else:            
            if task == self.active_tasks[-1]:
                if self.show_completed and len(self.completed_tasks):
                    next_entry = self.completed_tasks[0].textbox
                else:
                    next_entry = self.input_field
            else:
                active_index = self.active_tasks.index(task)
                next_entry = self.active_tasks[active_index + 1].textbox
            
            if next_entry != self.input_field:
                Util.scroll_into_view(self.master, next_entry)
            
            Util.shift_focus_from(task.textbox, next_entry)
            
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
