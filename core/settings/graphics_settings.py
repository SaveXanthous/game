from utils.json_handler import JSONHandler
from core.settings.base_settings import BaseSettings

class GraphicsSettings(BaseSettings):
    
    def __init__(self):
        super().__init__(self)

    # ----------------------------------------------------------------------------------------------------------------------------------------

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._fps

    @property
    def resolution(self):
        return (self._width, self._height)

    # -----------------------------------------------------------------------------------------------------------------------------------------

    @width.setter
    def width(self, value):
        self._width = value

    @height.setter
    def height(self, value):
        self._height = value

    @fps.setter
    def fps(self, value):
        self._fps = value

    # ----------------------------------------------------------------------------------------------------------------------------------------
    
    def set_settings(self, settings):
        path = JSONHandler.path_join('data', 'config', settings)

        screen_resolution = JSONHandler.get_by_key(path, "screen_resolution")
        WIDTH, HEIGHT = map(int, screen_resolution.split("x"))
        FPS = JSONHandler.get_by_key(path, "FPS")

        self.width = WIDTH
        self.height = HEIGHT
        self.fps = FPS