from events.default_events import DefaultEvents

class EventManager:

    __events = []

    @classmethod
    def init(cls, GameManager):
        cls.set_GameManager(GameManager)
        cls.add_event(DefaultEvents)

    @classmethod
    def set_GameManager(cls, GameManager):
        cls.__GameManager = GameManager

    @classmethod
    def add_event(cls, event):
        event.init(cls.__GameManager)
        cls.__events.append(event)

    @classmethod
    def remove_event(cls, event):
        cls.__events.remove(event)

    @classmethod
    def get_events(cls, event):
        return cls.__events
