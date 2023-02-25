from datetime import datetime


class BHDate():
    @staticmethod
    def from_str(date):
        return BHDate(int(date[:2]), int(date[3:5]), int(date[6:]))
    
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
    
    def __str__(self):
        return f'{self.day:02}/{self.month:02}/{self.year}'
    
    def serialize(self):
        return {'day': self.day, 'month': self.month, 'year': self.year}
    
    def set_date(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year
        
    def reset(self):
        self.day = self.month = self.year = None

    def is_set(self):
        return self.day and self.month and self.year

    def copy(self):
        return BHDate(self.day, self.month, self.year)
    
    def is_past(self, when):
        return when.date() > datetime.strptime(str(self), '%d/%m/%Y').date()
