from events.default_events import DefaultEvents
from core.game_handle import GameHandle

class EventsManager(GameHandle):

    
    def __init__(self, game_manager):
        GameHandle.__init__(self, game_manager)
        self._events = []
        self.add_event(DefaultEvents(self._game_manager))

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        self._events = value
    
    def add_event(self, event):
        self._events.append(event)
    
    def remove_event(self, event):
        self._events.remove(event)
