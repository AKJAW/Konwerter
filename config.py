import ConfigParser
import os.path

class Config:
    def __init__(self, path):
        self.path = path
        if not self.checkIfExists():
            self.createDefaultConfig()
        else:
            self.readFile()


    def checkIfExists(self):
        return os.path.exists(self.path)

    def createDefaultConfig(self):
        self.config = ConfigParser.ConfigParser()
        self.config.add_section("Settings")
        self.config.set("Settings", "font_size", "10")
        self.config.set("Settings", "arrow_size", "10")


    def createFile(self):
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def readFile(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path)

    def get(self, what):
        return self.config.get("Settings", what)

    def set(self, what, value):
        self.config.set("Settings", what, value)
        self.createFile()
