import os

class DirHandler(object):
    @staticmethod
    def get_dirs(path):
        return [e.name for e in os.scandir(path)]