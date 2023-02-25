from util import Util
from settings import Settings
from tasklist import TaskList
from bhdate import BHDate
from bhtime import BHTime
from datetimepicker import DateTimePicker

import customtkinter as ctk


class DarkModeSwitch(ctk.CTkSwitch):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.settings = master.master.settings

        if self.settings.appearance_mode == 'dark':
            self.select()
            
        self.configure(command=self.on_toggle)
            
    def on_toggle(self):
        if self.settings.appearance_mode == 'light':
            self.settings.appearance_mode = 'dark'
        else:
            self.settings.appearance_mode = 'light'
        
        ctk.set_appearance_mode(self.settings.appearance_mode)
        self.settings.write()


class Ballyhoo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme('dark-blue')

        self.title('Ballyhoo')
        self.geometry('500x400')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.configure(yscrollincrement=1)
        
        self.date = BHDate(None, None, None)
        self.time = BHTime(None, None)
        self.datetime_picker = None
        
        self.switch_frame = ctk.CTkFrame(master=self)
        self.show_completed_switch = ctk.CTkSwitch(master=self.switch_frame, text='Show Completed')
        self.dark_mode_switch = DarkModeSwitch(master=self.switch_frame, text='Dark Mode')
        self.input_field = ctk.CTkEntry(master=self)
        self.task_list = TaskList(master=self, input_field=self.input_field)
        self.datetime_picker_button = ctk.CTkButton(master=self, text='Pick DateTime')
        
        if self.settings.show_completed:
            self.show_completed_switch.select()
        self.show_completed_switch.configure(command=self.show_completed)
        
        self.input_field.bind(
            sequence='<Return>', 
            command=lambda event: self.add_task()
        )
        self.input_field.bind(
            sequence='<Up>', 
            command=lambda event: self.navigate_to_task_list()
        )
        self.input_field.bind(
            sequence='<Control-Key-a>', 
            command=lambda event, widget=self.input_field: Util.select_all(widget)
        )
        
        self.datetime_picker_button.configure(command=self.open_datetime_picker)
        
        self.switch_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.switch_frame.columnconfigure((0, 1), weight=1)
        self.show_completed_switch.grid(row=0, column=0, padx=10, pady=10)
        self.dark_mode_switch.grid(row=0, column=1, padx=10, pady=10)
        self.task_list.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        self.input_field.grid(row=2, column=0, padx=25, pady=(10, 20), sticky='ew')
        self.datetime_picker_button.grid(row=2, column=1, padx=25, pady=(10,20))
        
        self.input_field.focus()
        
    def show_completed(self):
        self.settings.show_completed = self.show_completed_switch.get()
        self.task_list.show_completed = self.settings.show_completed
        
        self.settings.write()
        self.task_list.update_task_list()
    
    def add_task(self):
        title = self.input_field.get()
        
        if title:
            self.task_list.add_task(title, self.date.copy(), self.time.copy())
            self.input_field.delete(0, ctk.END)
            self.date.reset()
            self.time.reset()
    
    def navigate_to_task_list(self):
        entry = None
        
        if self.settings.show_completed and len(self.task_list.completed_tasks):
            entry = self.task_list.completed_tasks[-1].entry
        elif len(self.task_list.active_tasks):
            entry = self.task_list.active_tasks[-1].entry
        
        if entry:
            Util.scroll_into_view(self.task_list.master, entry)
            Util.shift_focus_from(self.input_field, entry)
            
    def open_datetime_picker(self):
        if self.datetime_picker:
            self.datetime_picker.lift()
            self.datetime_picker.focus()
        else:
            self.datetime_picker = DateTimePicker(master=self, date=self.date, time=self.time)
        
        self.datetime_picker = None
