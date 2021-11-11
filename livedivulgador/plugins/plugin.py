from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def run(self):
        ...

    def stop(self):
        ...
