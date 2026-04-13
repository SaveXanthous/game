from abc import ABC, abstractmethod

class BaseEvents(ABC):
    @classmethod
    def init(cls, GameManager):
        cls.set_GameManager(GameManager)

    @classmethod
    def set_GameManager(cls, GameManager):
        cls._GameManager = GameManager

    @classmethod
    @abstractmethod
    def process(cls, event):
        pass