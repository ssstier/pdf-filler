import os
import configparser


class Options:
    def __init__(self):
        self.project_dir = os.path.dirname(os.getcwd())
        self.settings = os.path.join(self.project_dir, r"config\settings.ini")
        self.cache = self.get_settings()
        self.big_font = ("Helvetica", 16)
        self.regular_font = ("Cosmic Sans", 14)

    def get_settings(self):
        config = configparser.ConfigParser()
        config.read(self.settings)
        return {s: dict(config.items(s)) for s in config.keys()}

    def set_settings(self, section, key, new_value):
        config = configparser.ConfigParser()
        config.read(self.settings)
        config.set(section, key, new_value)
        with open(self.settings, 'w') as configfile:
            config.write(configfile)
            self.cache = {s: dict(config.items(s)) for s in config.keys()}
