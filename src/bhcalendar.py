from bhdate import BHDate

import customtkinter as ctk
import calendar


class BHCalendar(ctk.CTkFrame):
    def __init__(self, master, datetime, date, **kwargs):
        super().__init__(master, **kwargs)
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure((0, 1), weight=1)
        
        self.day = datetime.day
        self.month = datetime.month
        self.year = datetime.year
        self.date = date
        self.weekdays = ['Mon', 'Tue', 'Wen', 'Thu', 'Fri', 'Sat', 'Sun']
        self.months = {month: i for i, month in enumerate(calendar.month_name)}
        self.last_pressed = None
        
        self.month_picker = ctk.CTkOptionMenu(
            master=self, 
            values=calendar.month_name[1:],
            command=self.update_month
        )
        self.year_picker = ctk.CTkOptionMenu(
            master=self, 
            values=[str(i) for i in range(self.year, self.year + 10)],
            command=self.update_year
        )
        self.day_picker = ctk.CTkFrame(master=self)
        self.save_button = ctk.CTkButton(master=self, text='Save', command=self.save_date)
        
        self.day_picker.columnconfigure(
            [i for i in range(0, len(self.weekdays))],
            weight=1
        )
        
        self.month_picker.set(calendar.month_name[self.month])
        self.year_picker.set(str(self.year))

        self.month_picker.grid(row=0, column=0)
        self.year_picker.grid(row=0, column=1)
        self.day_picker.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.save_button.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 5))
        
        self.update_day_picker()
    
    def update_day_picker(self):
        for child in self.day_picker.winfo_children():
            child.destroy()
            
        for i, weekday in enumerate(self.weekdays):
            label = ctk.CTkLabel(master=self.day_picker, text=weekday)
            
            label.grid(row=0, column=i, padx=10, pady=(10, 0), sticky='nsew')
            
        for i, week in enumerate(calendar.monthcalendar(self.year, self.month)):
            for j, day in enumerate(week):
                button = ctk.CTkButton(
                    master=self.day_picker, 
                    corner_radius=0,
                    fg_color='gray',
                    text=day if day else '', 
                    state='normal' if day else 'disabled' 
                )
                
                button.configure(command=lambda widget=button: self.update_day(widget))
                button.grid(row=i + 1, column=j, padx=2, pady=2)

    def update_month(self, month):
        if self.month != self.months[month]:
            self.month = self.months[month]
            self.update_day_picker()
    
    def update_year(self, year):
        if self.year != int(year):
            self.year = int(year)
            self.update_day_picker()
            
    def save_date(self):
        self.date.set_date(self.day, self.month, self.year)
    
    def update_day(self, widget):
        self.day = int(widget.cget('text'))
        
        if self.last_pressed:
            self.last_pressed.configure(fg_color='gray')
            
        self.last_pressed = widget
        
        widget.configure(fg_color=widget.cget('hover_color'))
