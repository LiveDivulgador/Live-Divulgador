from abc import ABC
from collections import deque
from live_divulgator.plugins.plugin import Plugin


class Bot(ABC):
    def __init__(self) -> None:
        self.plugins: list[Plugin] = []

    def add_plugin(self, plugin: Plugin) -> None:
        self.plugins.append(plugin)

    def add_plugins(self, plugins: list[Plugin]) -> None:
        list(map(self.add_plugin, plugins))

    def load_plugins(self) -> None:
        runner = lambda plugin: plugin.run()
        list(map(runner, self.plugins))

    def run(self) -> None:
        self.load_plugins()
