import os
import configparser


class Options:
    def __init__(self):
        self.project_dir = os.path.dirname(os.getcwd())
        self.startup = self.get_settings
        self.settings = os.path.join(self.project_dir, 'config\settings.ini')
        self.big_font = ("Helvetica", 16)
        self.regular_font = ("Cosmic Sans", 14)

    def read_file(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(self.project_dir, 'config\settings.ini'))
        return config
        
    def get_settings(self):
        config = self.read_file()
        return {s:dict(config.items(s)) for s in config.keys()}

    def set_settings(self, config, section, key, new_value):
        config = self.read_file()
        config.set(section, key, new_value)
        with open(self.settings, 'w') as configfile:
            config.write(configfile)
    
