from core.settings.graphics_settings import GraphicsSettings


class SettingsManager:
    def __init__(self):
        self._graphics_settings = GraphicsSettings()

    @property
    def graphics_settings(self):
        return self._graphics_settings

    @graphics_settings.setter
    def graphics_settings(self, value):
        self._graphics_settings = value
