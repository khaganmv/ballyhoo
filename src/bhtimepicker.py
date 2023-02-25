import customtkinter as ctk


class BHTimePicker(ctk.CTkFrame):
    def __init__(self, master, datetime, date, time, **kwargs):
        super().__init__(master, **kwargs)
        
        self.day = datetime.day
        self.month = datetime.month
        self.year = datetime.year
        self.hour = datetime.hour
        self.minute = datetime.minute
        self.date = date
        self.time = time
        
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        
        self.hour_picker = ctk.CTkLabel(
            master=self, 
            text=f'{self.hour:02}', 
            font=('default', 32), 
            justify='center'
        )
        self.minute_picker = ctk.CTkLabel(
            master=self, 
            text=f'{self.minute:02}', 
            font=('default', 32), 
            justify='center'
        )
        
        self.colon = ctk.CTkLabel(master=self, text=':', font=('default', 32))
        
        self.hour_button_inc = ctk.CTkButton(
            master=self, 
            text='+', 
            command=lambda by=1: self.increment_hour(by)
        )
        self.hour_button_dec = ctk.CTkButton(
            master=self, 
            text='-', 
            command=lambda by=-1: self.increment_hour(by)
        )
        self.minute_button_inc = ctk.CTkButton(
            master=self, 
            text='+', 
            command=lambda by=1: self.increment_minute(by)
        )
        self.minute_button_dec = ctk.CTkButton(
            master=self, 
            text='-', 
            command=lambda by=-1: self.increment_minute(by)
        )
        self.save_button = ctk.CTkButton(
            master=self, 
            text='Save', 
            command=self.save_time
        )
        
        self.hour_button_inc.grid(row=0, column=0, padx=(20, 0), sticky='ew')
        self.hour_picker.grid(row=1, column=0, padx=(20, 0), sticky='ew')
        self.hour_button_dec.grid(row=2, column=0, padx=(20, 0), sticky='ew')
        self.colon.grid(row=1, column=1, sticky='ew')
        self.minute_button_inc.grid(row=0, column=2, padx=(0, 20), sticky='ew')
        self.minute_picker.grid(row=1, column=2, padx=(0, 20), sticky='ew')
        self.minute_button_dec.grid(row=2, column=2, padx=(0, 20), sticky='ew')
        self.save_button.grid(row=3, column=0, columnspan=3)
                
    def increment_hour(self, by):
        if self.hour_picker.cget('text').isdigit():
            hour = int(self.hour_picker.cget('text')) + by
            self.hour = hour % 24 if hour < 0 or hour > 23 else hour

            self.hour_picker.configure(text=f'{self.hour:02}')

    def increment_minute(self, by):
        if self.minute_picker.cget('text').isdigit():
            minute = int(self.minute_picker.cget('text')) + by
            self.minute = minute % 60 if minute < 0 or minute > 59 else minute

            self.minute_picker.configure(text=f'{self.minute:02}')
    
    def save_time(self):
        if not self.date.is_set():
            self.date.set_date(self.day, self.month, self.year)
            
        self.time.set_time(self.hour, self.minute)
