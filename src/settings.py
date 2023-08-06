import json

class Settings():
    def __init__(self, dir):
        self.dir = dir
        self.width, self.height, self.show_completed, self.appearance_mode = self.read()
        
    def serialize(self):
        return { 
            'width': self.width, 
            'height': self.height, 
            'show_completed': self.show_completed, 
            'appearance_mode': self.appearance_mode 
        }

    def read(self):
        width = 500
        height = 400
        show_completed = False
        appearance_mode = 'dark'
        
        with open(self.dir + 'settings.json', 'a+') as settings_file:
            if settings_file.tell():
                settings_file.seek(0)
                data = json.load(settings_file)
                width = data['width']
                height = data['height']
                show_completed = data['show_completed']
                appearance_mode = data['appearance_mode']
        
        return width, height, show_completed, appearance_mode
    
    def write(self):
        with open(self.dir + 'settings.json', 'w') as settings_file:
            json.dump(self.serialize(), settings_file, indent=4)
