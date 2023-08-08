from util import Util
from settings import Settings
from tasklist import TaskList

import customtkinter as ctk
import os
from PIL import Image
import pystray
import shutil


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

        # dir = './'
        dir = os.getenv('LOCALAPPDATA') + '/Ballyhoo/'
        
        if not os.path.isdir(dir):
            os.mkdir(dir)
            
        self.start_menu_dir = os.getenv('APPDATA') + '/Microsoft/Windows/Start Menu/Programs/'
        
        self.settings = Settings(dir)
        self.font = ctk.CTkFont('fixedsys', 12)
        self.settings_open = False
        
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme('dark-blue')

        self.title('Ballyhoo')
        self.geometry(f'{self.settings.width}x{self.settings.height}')
        self.iconbitmap(Util.resource_path('ballyhoo.ico'))
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.configure(yscrollincrement=1)
        Util.center(self)
        
        self.switch_frame = ctk.CTkFrame(master=self)
        self.switch_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.switch_frame.columnconfigure(0, weight=1)
        
        self.show_completed_switch = ctk.CTkSwitch(master=self.switch_frame, text='Show Completed Tasks', font=self.font)
        self.dark_mode_switch = DarkModeSwitch(master=self.switch_frame, text='Dark Mode', font=self.font)
        self.minimize_to_tray_switch = ctk.CTkSwitch(master=self.switch_frame, text='Minimize to Tray', font=self.font)
        self.run_on_startup_switch = ctk.CTkSwitch(master=self.switch_frame, text='Run on Startup', font=self.font)
        self.input_field = ctk.CTkEntry(master=self, font=self.font)
        self.task_list = TaskList(master=self, dir=dir, input_field=self.input_field)
        
        BUTTON_WIDTH = BUTTON_HEIGHT = 30
        settings_icon_light = Image.open(Util.resource_path('settings_light.png'))
        settings_icon_dark = Image.open(Util.resource_path('settings_dark.png'))
        
        self.settings_button = ctk.CTkButton(
            master=self, 
            width=28, 
            height=28, 
            text=None,
            fg_color='transparent',
            image=ctk.CTkImage(settings_icon_light, settings_icon_dark, size=(BUTTON_WIDTH, BUTTON_HEIGHT)),
            command=self.open_settings
        )
        
        if self.settings.show_completed:
            self.show_completed_switch.select()
        self.show_completed_switch.configure(command=self.show_completed)
        
        if self.settings.minimize_to_tray:
            self.minimize_to_tray_switch.select()
            self.protocol('WM_DELETE_WINDOW', self.bh_withdraw)
        self.minimize_to_tray_switch.configure(command=self.minimize_to_tray)
        
        if self.settings.run_on_startup:
            self.run_on_startup_switch.select()
        self.run_on_startup_switch.configure(command=self.run_on_startup)
        
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
            command=lambda event: self.navigate_to_task_list(True)
        )
        self.input_field.bind(
            sequence='<Control-Key-a>', 
            command=lambda event, widget=self.input_field: Util.select_all(widget)
        )
        
        self.show_completed_switch.grid(row=0, column=0, padx=10, sticky='nsew')
        self.dark_mode_switch.grid(row=1, column=0, padx=10, sticky='nsew')
        self.minimize_to_tray_switch.grid(row=2, column=0, padx=10, sticky='nsew')
        self.run_on_startup_switch.grid(row=3, column=0, padx=10, sticky='nsew')
        self.task_list.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nsew')
        self.input_field.grid(row=1, column=0, padx=(20, 0), pady=(10, 20), sticky='ew')
        self.settings_button.grid(row=1, column=1, padx=(10, 15), pady=(10, 20))
        
        self.update_idletasks()
        self.navigate_to_task_list()
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
        if event.widget == self and (event.width != self.settings.width or event.height != self.settings.height):
            self.settings.width = event.width
            self.settings.height = event.height
            self.settings.write()

    def run_on_startup(self):
        self.settings.run_on_startup = self.run_on_startup_switch.get()
        
        try:
            if self.settings.run_on_startup:
                shutil.copy2(self.start_menu_dir + 'Ballyhoo/Ballyhoo.lnk', self.start_menu_dir + 'Startup/')
            else:
                os.remove(self.start_menu_dir + 'Startup/Ballyhoo.lnk')
        except:
            pass
        
        self.settings.write()

    def open_settings(self):
        if self.settings_open:
            self.switch_frame.grid_forget()
            self.task_list.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nsew')
        else:
            self.task_list.grid_forget()
            self.switch_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='new')
            
        self.settings_open = not self.settings_open

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
    
    def navigate_to_task_list(self, shift_focus=False):
        entry = None
        
        if self.settings.show_completed and len(self.task_list.completed_tasks):
            entry = self.task_list.completed_tasks[-1].entry
        elif len(self.task_list.active_tasks):
            entry = self.task_list.active_tasks[-1].entry
        
        if entry:
            Util.scroll_into_view(self.task_list.master, entry)
            
            if shift_focus:
                Util.shift_focus_from(self.input_field, entry)
