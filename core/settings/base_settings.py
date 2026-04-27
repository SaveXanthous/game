from abc import ABC, abstractmethod

class BaseSettings(ABC):

    def __init__(self, game_manager):
        self._name_settings = "user_settings.json"
        self.set_settings(self._name_settings)

    @property
    def name_settings(self):
        return self._name_settings

    @name_settings.setter
    def name_settings(self, name_settings):
        self._name_settings = name_settings

    @abstractmethod
    def set_settings(self, name_settings):
        pass