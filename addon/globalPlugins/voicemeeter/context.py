from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, controller, index):
        self._controller = controller
        self._index = index

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val

    def get_bool(self, param: str) -> bool:
        return self._controller._get(f"{self.identifier}.{param}") == 1

    def set_bool(self, param: str, val: bool):
        self._controller._set(f"{self.identifier}.{param}", 1 if val else 0)


class StripStrategy(Strategy):
    def __str__(self):
        return "Strip"

    @property
    def identifier(self):
        return f"strip[{self._index}]"


class BusStrategy(Strategy):
    def __str__(self):
        return "Bus"

    @property
    def identifier(self):
        return f"bus[{self._index}]"


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def index(self):
        return self._strategy._index

    @index.setter
    def index(self, val):
        self._strategy._index = val

    def get_bool(self, *args):
        return self._strategy.get_bool(*args)

    def set_bool(self, *args):
        self._strategy.set_bool(*args)
