import json

class Settings():
    def __init__(self):
        sc, am = self.read_settings()
        
        self.sc = sc if sc else False
        self.am = am if am else 'dark'
        
    def serialize(self):
        return { 'sc': self.sc, 'am': self.am }

    def read_settings(self):
        sc = am = None
        
        sf = open('settings.json', 'a+')
        if sf.tell():
            sf.seek(0)
            data = json.load(sf)
            sc, am = data['sc'], data['am']
        sf.close()
        
        return sc, am
    
    def write_settings(self):
        sf = open('settings.json', 'w')
        json.dump(self.serialize(), sf)
        sf.close()