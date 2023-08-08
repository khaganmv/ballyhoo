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
        self.font = ctk.CTkFont('fixedsys', 56)
        
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        
        self.hour_label = ctk.CTkLabel(
            master=self, 
            text=f'{self.hour:02}', 
            justify='center',
            font=self.font,
            fg_color='transparent'
        )
        self.colon_label = ctk.CTkLabel(
            master=self, 
            text=':', 
            font=self.font,
            fg_color='transparent'
        )
        self.minute_label = ctk.CTkLabel(
            master=self, 
            text=f'{self.minute:02}', 
            justify='center',
            font=self.font,
            fg_color='transparent'
        )
        
        self.hour_label.bind(
            '<MouseWheel>',
            command=lambda event: self.increment_hour(event)
        )
        self.minute_label.bind(
            '<MouseWheel>',
            command=lambda event: self.increment_minute(event)
        )

        self.hour_label.grid(row=1, column=0, sticky='nsew')
        self.colon_label.grid(row=1, column=1, sticky='nsew')
        self.minute_label.grid(row=1, column=2, sticky='nsew')
        
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
