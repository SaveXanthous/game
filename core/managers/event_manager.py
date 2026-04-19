from events.default_events import DefaultEvents

class EventManager:

    
    def __init__(self, game_manager):
        self._events = []
        self._game_manager = game_manager
        self.add_event(DefaultEvents(self._game_manager))

    @property
    def game_manager(self):
        return self._game_manager

    @property
    def events(self):
        return self._events

    @game_manager.setter
    def game_manager(self, value):
        self._game_manager = value

    @events.setter
    def events(self, value):
        self._events = value
    
    def add_event(self, event):
        self._events.append(event)
    
    def remove_event(self, event):
        self._events.remove(event)
