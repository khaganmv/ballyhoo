from util import Util
from settings import Settings
from tasklist import TaskList

import customtkinter as ctk
import os
from PIL import Image
import pystray


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

        dir = os.getenv('LOCALAPPDATA') + '/Ballyhoo/'
        # dir = './'
        
        if not os.path.isdir(dir):
            os.mkdir(dir)
        
        self.settings = Settings(dir)
        self.font = ctk.CTkFont('fixedsys', 12)
        
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme('dark-blue')

        self.title('Ballyhoo')
        self.geometry(f'{self.settings.width}x{self.settings.height}')
        self.iconbitmap(Util.resource_path('ballyhoo.ico'))
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.configure(yscrollincrement=1)
        Util.center(self)
        
        self.switch_frame = ctk.CTkFrame(master=self)
        self.switch_frame.columnconfigure((0, 1, 2), weight=1)
        
        self.show_completed_switch = ctk.CTkSwitch(master=self.switch_frame, text='Show Completed', font=self.font)
        self.dark_mode_switch = DarkModeSwitch(master=self.switch_frame, text='Dark Mode', font=self.font)
        self.minimize_to_tray_switch = ctk.CTkSwitch(master=self.switch_frame, text='Minimize to Tray', font=self.font)
        self.input_field = ctk.CTkEntry(master=self, font=self.font)
        self.task_list = TaskList(master=self, dir=dir, input_field=self.input_field)
        
        if self.settings.show_completed:
            self.show_completed_switch.select()
        self.show_completed_switch.configure(command=self.show_completed)
        
        if self.settings.minimize_to_tray:
            self.minimize_to_tray_switch.select()
            self.protocol('WM_DELETE_WINDOW', self.bh_withdraw)
        self.minimize_to_tray_switch.configure(command=self.minimize_to_tray)
        
        self.bind(
            sequence='<Configure>', 
            func=lambda event: self.resize(event)
        )
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
        
        self.switch_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.show_completed_switch.grid(row=0, column=0, padx=10, pady=10)
        self.dark_mode_switch.grid(row=0, column=1, padx=10, pady=10)
        self.minimize_to_tray_switch.grid(row=0, column=2, padx=10, pady=10)
        self.task_list.grid(row=1, column=0, columnspan=2, padx=20, sticky='nsew')
        self.input_field.grid(row=2, column=0, padx=25, pady=(10, 20), sticky='ew')
        
        self.input_field.focus()
    
    def minimize_to_tray(self):
        self.settings.minimize_to_tray = self.minimize_to_tray_switch.get()
        self.protocol('WM_DELETE_WINDOW', self.bh_withdraw if self.settings.minimize_to_tray else self.destroy)
        self.settings.write()
    
    def bh_show(self, icon):
        icon.stop()
        self.after(0, self.deiconify)

    def bh_quit(self, icon):
        icon.stop()
        self.destroy()

    def bh_withdraw(self):
        self.withdraw()
        image = Image.open(Util.resource_path('ballyhoo.ico'))
        menu = (
            pystray.MenuItem('Show', lambda icon, item: self.bh_show(icon)), 
            pystray.MenuItem('Quit', lambda icon, item: self.bh_quit(icon))
        )
        icon = pystray.Icon('ballyhoo', image, 'Ballyhoo', menu)
        icon.run()
    
    def resize(self, event):
        if event.widget == self:
            if event.width != self.settings.width or event.height != self.settings.height:
                self.settings.width = event.width
                self.settings.height = event.height
                
                self.settings.write()

    def show_completed(self):
        self.settings.show_completed = self.show_completed_switch.get()
        self.task_list.show_completed = self.settings.show_completed
        
        self.settings.write()
        self.task_list.update_task_list()
    
    def add_task(self):
        title = self.input_field.get()
        
        if title:
            self.task_list.add_task(title)
            self.input_field.delete(0, ctk.END)
    
    def navigate_to_task_list(self):
        entry = None
        
        if self.settings.show_completed and len(self.task_list.completed_tasks):
            entry = self.task_list.completed_tasks[-1].entry
        elif len(self.task_list.active_tasks):
            entry = self.task_list.active_tasks[-1].entry
        
        if entry:
            Util.scroll_into_view(self.task_list.master, entry)
            Util.shift_focus_from(self.input_field, entry)
