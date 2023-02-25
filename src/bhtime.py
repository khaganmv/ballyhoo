from datetime import datetime


class BHTime():
    @staticmethod
    def from_str(time):
        return BHTime(int(time[:2]), int(time[3:]))
    
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute
    
    def __str__(self):
        return f'{self.hour:02}:{self.minute:02}'
    
    def serialize(self):
        return {'hour': self.hour, 'minute': self.minute}
    
    def set_time(self, hour, minute):
        self.hour = hour
        self.minute = minute
        
    def reset(self):
        self.hour = self.minute = None

    def is_set(self):
        return self.hour and self.minute

    def copy(self):
        return BHTime(self.hour, self.minute)

    def is_past(self, when):
        return when.time() > datetime.strptime(str(self), '%H:%M').time()
