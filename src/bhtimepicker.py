import customtkinter as ctk


class BHTimePicker(ctk.CTkFrame):
    def __init__(self, master, datetime, task, **kwargs):
        super().__init__(master, **kwargs)
        
        self.task = task
        self.date = task.date
        self.time = task.time
        self.day = datetime.day
        self.month = datetime.month
        self.year = datetime.year
        self.hour = task.time.hour if task.time.is_set() else datetime.hour
        self.minute = task.time.minute if task.time.is_set() else datetime.minute
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.clock = ctk.CTkFrame(master=self,fg_color=('white', '#4C4E52'))
        self.clock.rowconfigure(0, weight=1)
        self.clock.columnconfigure((0, 1, 2), weight=1)
        
        self.hour_label = ctk.CTkLabel(
            master=self.clock, 
            text=f'{self.hour:02}', 
            font=('default', 32), 
            justify='center'
        )
        self.colon_label = ctk.CTkLabel(
            master=self.clock, 
            text=':', 
            font=('default', 32)
        )
        self.minute_label = ctk.CTkLabel(
            master=self.clock, 
            text=f'{self.minute:02}', 
            font=('default', 32), 
            justify='center'
        )
        
        self.hour_label.bind(
            '<MouseWheel>',
            command=lambda event: self.increment_hour(event)
        )
        self.minute_label.bind(
            '<MouseWheel>',
            command=lambda event: self.increment_minute(event)
        )

        self.clock.grid(row=0, column=0, padx=(40, 40), pady=(40, 40), sticky='nsew')
        self.hour_label.grid(row=0, column=0, sticky='nsew')
        self.colon_label.grid(row=0, column=1, sticky='nsew')
        self.minute_label.grid(row=0, column=2, sticky='nsew')
                
    def increment_hour(self, event):
        if self.hour_label.cget('text').isdigit():
            by = 1 if event.delta > 0 else -1
            hour = int(self.hour_label.cget('text')) + by
            self.hour = hour % 24 if hour < 0 or hour > 23 else hour

            self.hour_label.configure(text=f'{self.hour:02}')

    def increment_minute(self, event):
        if self.minute_label.cget('text').isdigit():
            by = 1 if event.delta > 0 else -1
            minute = int(self.minute_label.cget('text')) + by
            self.minute = minute % 60 if minute < 0 or minute > 59 else minute

            self.minute_label.configure(text=f'{self.minute:02}')
