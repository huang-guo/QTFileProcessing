import configparser


class Config:
    _conf = configparser.ConfigParser()
    _conf.read('./app.ini', encoding="utf-8")

    def __init__(self, section):
        self.section = section

    def get(self, key):
        return self._conf.get(self.section, key)

    def set(self, key, value):
        self._conf.set(self.section, key, value)
        with open("./app.ini", "w+") as f:
            self._conf.write(f)

    @classmethod
    def reload(cls):
        cls._conf.read('./app.ini', encoding="utf-8")
