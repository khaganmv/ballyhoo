import json


class Settings():
    def __init__(self):
        show_completed, appearance_mode = self.read()
        
        self.show_completed = show_completed if show_completed else False
        self.appearance_mode = appearance_mode if appearance_mode else 'dark'
        
    def serialize(self):
        return { 'show_completed': self.show_completed, 'appearance_mode': self.appearance_mode }

    def read(self):
        show_completed = appearance_mode = None
        
        with open('settings.json', 'a+') as settings_file:
            if settings_file.tell():
                settings_file.seek(0)
                data = json.load(settings_file)
                show_completed, appearance_mode = data['show_completed'], data['appearance_mode']
                
            settings_file.close()
        
        return show_completed, appearance_mode
    
    def write(self):
        with open('settings.json', 'w') as settings_file:
            json.dump(self.serialize(), settings_file)
            settings_file.close()
