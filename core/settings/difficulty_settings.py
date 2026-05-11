from utils.json_handler import JSONHandler
from core.settings.base_settings import BaseSettings

class DifficultySettings(BaseSettings):

    def __init__(self):
        super().__init__(self)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    def set_settings(self, name_settings):
        path = JSONHandler.path_join('data', 'config', name_settings)
        self._difficulty = JSONHandler.get_by_key(path, 'difficulty')
