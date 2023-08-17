import os
import pystray
import shutil
import win32com.client

import customtkinter as ctk
from PIL import Image

from util import Util
from settings import Settings
from tasklist import TaskList
from settingsmenu import SettingsMenu


class Ballyhoo(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        release = True

        # init self
        self.dir = os.getenv('LOCALAPPDATA') + '/Ballyhoo/' if release else './'
        self.start_menu_dir = os.getenv('APPDATA') + '/Microsoft/Windows/Start Menu/Programs/'
        
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        
        self.settings = Settings(self.dir)
        self.font = ctk.CTkFont('fixedsys', 12)
        self.settings_icon = ctk.CTkImage(
            Image.open(Util.resource_path('settings_light.png')), 
            Image.open(Util.resource_path('settings_dark.png')), 
            size=(30, 30)
        )
        self.on_settings_menu = False
        
        if self.settings.minimize_to_tray:
            self.protocol('WM_DELETE_WINDOW', self.withdraw_to_tray)
            
        if self.settings.start_minimized:
            self.withdraw_to_tray()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # init window
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme('dark-blue')

        self.title('Ballyhoo')
        self.geometry(f'{self.settings.width}x{self.settings.height}')
        self.iconbitmap(Util.resource_path('ballyhoo.ico'))
        self.configure(yscrollincrement=1)
        Util.center(self)
        
        # init widgets
        self.settings_menu = SettingsMenu(master=self)
        self.input_field = ctk.CTkEntry(master=self, font=self.font)
        self.task_list = TaskList(master=self, dir=self.dir, input_field=self.input_field)
        self.settings_button = ctk.CTkButton(
            master=self, 
            width=28, 
            height=28, 
            text=None,
            fg_color='transparent',
            image=self.settings_icon,
            command=self.open_settings_menu
        )
        
        # init bindings
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
        
        # init layout
        self.task_list.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nsew')
        self.input_field.grid(row=1, column=0, padx=(20, 0), pady=(10, 20), sticky='ew')
        self.settings_button.grid(row=1, column=1, padx=(10, 15), pady=(10, 20))
        
        self.update_idletasks()
        self.task_list.update_task_list()
        self.task_list.resize_textboxes()
        self.navigate_to_task_list()
        self.poll_task_list()
        self.input_field.focus()
        
    def add_task(self):
        title = self.input_field.get()
        
        if title:
            self.task_list.add_task(title)
            self.input_field.delete(0, ctk.END)
    
    def navigate_to_task_list(self, shift_focus=False):
        entry = None
        
        if self.settings.show_completed and len(self.task_list.completed_tasks):
            entry = self.task_list.completed_tasks[-1].textbox
        elif len(self.task_list.active_tasks):
            entry = self.task_list.active_tasks[-1].textbox
        
        if entry:
            Util.scroll_into_view(self.task_list.master, entry)
            
            if shift_focus:
                Util.shift_focus_from(self.input_field, entry)
                
    def resize(self, event):
        if event.widget == self and (event.width != self.settings.width or event.height != self.settings.height):
            self.settings.width = event.width
            self.settings.height = event.height
            self.settings.write()

    def open_settings_menu(self, button=True):
        if self.on_settings_menu or not button:
            self.settings_menu.grid_forget()
            self.task_list.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='nsew')
        else:
            self.task_list.grid_forget()
            self.settings_menu.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky='new')
        
        if button:
            self.on_settings_menu = not self.on_settings_menu
        else:
            self.on_settings_menu = False

    def poll_task_list(self):
        self.task_list.update_datetime_labels()
        self.after(1000, self.poll_task_list)

    def show_completed(self):
        self.settings.show_completed = self.settings_menu.show_completed_switch.get()
        self.task_list.show_completed = self.settings.show_completed
        self.settings.write()
        self.task_list.update_task_list()

    def switch_appearance_mode(self):
        if self.settings.appearance_mode == 'light':
            self.settings.appearance_mode = 'dark'
        else:
            self.settings.appearance_mode = 'light'
        
        ctk.set_appearance_mode(self.settings.appearance_mode)
        self.settings.write()

    def run_on_startup(self):
        self.settings.run_on_startup = self.settings_menu.run_on_startup_switch.get()
        
        try:
            if self.settings.run_on_startup:
                if os.path.isfile(self.start_menu_dir + 'Ballyhoo/Ballyhoo.lnk'):
                    shutil.copy2(self.start_menu_dir + 'Ballyhoo/Ballyhoo.lnk', self.start_menu_dir + 'Startup/')
                else:
                    shell = win32com.client.Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortcut(self.start_menu_dir + 'Startup/Ballyhoo.lnk')
                    shortcut.Targetpath = os.environ['ProgramFiles(x86)'] + '/Ballyhoo/ballyhoo.exe'
                    shortcut.IconLocation = Util.resource_path('ballyhoo.ico')
                    shortcut.save()
            else:
                os.remove(self.start_menu_dir + 'Startup/Ballyhoo.lnk')
        except:
            pass
        
        self.settings.write()

    def show(self, icon):
        icon.stop()
        self.after(0, self.deiconify)

    def exit(self, icon):
        icon.stop()
        self.destroy()

    def withdraw_to_tray(self):
        self.withdraw()
        self.open_settings_menu(button=False)
        
        image = Image.open(Util.resource_path('ballyhoo.ico'))
        menu = (pystray.MenuItem('Show', lambda icon, item: self.show(icon)), 
                pystray.MenuItem('Exit', lambda icon, item: self.exit(icon)))
        icon = pystray.Icon('ballyhoo', image, 'Ballyhoo', menu)
        
        icon.run()

    def minimize_to_tray(self):
        self.settings.minimize_to_tray = self.settings_menu.minimize_to_tray_switch.get()
        self.protocol('WM_DELETE_WINDOW', self.withdraw_to_tray if self.settings.minimize_to_tray else self.destroy)
        self.settings.write()
        
    def start_minimized(self):
        self.settings.start_minimized = self.settings_menu.start_minimized_switch.get()
        self.settings.write()
    