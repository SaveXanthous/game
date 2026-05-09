class GameHandle:
    def __init__(self,game_manager):
        self._game_manager = game_manager

    @property
    def game_manager(self):
        return self._game_manager
    
    @game_manager.setter
    def game_manager(self,game_manager):
        self._game_manager = game_manager