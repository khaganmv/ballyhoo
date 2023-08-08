import json

class Settings():
    def __init__(self, dir):
        self.dir = dir
        self.appearance_mode, self.width, self.height, \
        self.show_completed, self.minimize_to_tray, self.run_on_startup = self.read()
        
    def serialize(self):
        return { 
            'appearance_mode': self.appearance_mode,
            'width': self.width, 
            'height': self.height, 
            'show_completed': self.show_completed, 
            'minimize_to_tray': self.minimize_to_tray,
            'run_on_startup': self.run_on_startup
        }

    def read(self):
        appearance_mode = 'dark'
        width = 600
        height = 500
        show_completed = minimize_to_tray = run_on_startup = False
        
        with open(self.dir + 'settings.json', 'a+') as settings_file:
            if settings_file.tell():
                settings_file.seek(0)
                data = json.load(settings_file)
                appearance_mode = data['appearance_mode']
                width = data['width']
                height = data['height']
                show_completed = data['show_completed']
                minimize_to_tray = data['minimize_to_tray']
                run_on_startup = data['run_on_startup']
        
        return appearance_mode, width, height, show_completed, minimize_to_tray, run_on_startup
    
    def write(self):
        with open(self.dir + 'settings.json', 'w') as settings_file:
            json.dump(self.serialize(), settings_file, indent=4)
