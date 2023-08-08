import customtkinter as ctk

        
class SettingsMenu(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # init self
        self.settings = master.settings
        self.font = ctk.CTkFont('fixedsys', 12)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4), weight=1)
        
        # init widgets
        self.show_completed_switch = ctk.CTkSwitch(master=self, text='Show Completed Tasks', font=self.font)
        self.dark_mode_switch = ctk.CTkSwitch(master=self, text='Dark Mode', font=self.font)
        self.minimize_to_tray_switch = ctk.CTkSwitch(master=self, text='Minimize to System Tray', font=self.font)
        self.run_on_startup_switch = ctk.CTkSwitch(master=self, text='Run on Startup', font=self.font)
        self.start_minimized_switch = ctk.CTkSwitch(master=self, text='Start Minimized', font=self.font)
        
        if self.settings.show_completed:
            self.show_completed_switch.select()
        self.show_completed_switch.configure(command=self.master.show_completed)
        
        if self.settings.appearance_mode == 'dark':
            self.dark_mode_switch.select()
        self.dark_mode_switch.configure(command=self.master.switch_appearance_mode)
        
        if self.settings.minimize_to_tray:
            self.minimize_to_tray_switch.select()
        self.minimize_to_tray_switch.configure(command=self.master.minimize_to_tray)
        
        if self.settings.run_on_startup:
            self.run_on_startup_switch.select()
        self.run_on_startup_switch.configure(command=self.master.run_on_startup)
        
        if self.settings.start_minimized:
            self.start_minimized_switch.select()
        self.start_minimized_switch.configure(command=self.master.start_minimized)
        
        # init layout
        self.show_completed_switch.grid(row=0, column=0, padx=10, sticky='nsew')
        self.dark_mode_switch.grid(row=1, column=0, padx=10, sticky='nsew')
        self.minimize_to_tray_switch.grid(row=2, column=0, padx=10, sticky='nsew')
        self.run_on_startup_switch.grid(row=3, column=0, padx=10, sticky='nsew')
        self.start_minimized_switch.grid(row=4, column=0, padx=10, sticky='nsew')
