from core.settings.graphics_settings import GraphicsSettings
from settings.difficulty_settings import DifficultySettings


class SettingsManager:
    def __init__(self):
        self._graphics_settings = GraphicsSettings()
        self._difficulty_settings = DifficultySettings()

    @property
    def graphics_settings(self):
        return self._graphics_settings

    @property
    def difficulty_settings(self):
        return self._difficulty_settings

    @graphics_settings.setter
    def graphics_settings(self, value):
        self._graphics_settings = value

    @difficulty_settings.setter
    def difficulty_settings(self, value):
        self._difficulty_settings = value
