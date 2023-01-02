import os

class Path(str):
    def __new__(cls, *args):
        obj = super().__new__(cls, os.path.join(*args))
        return obj