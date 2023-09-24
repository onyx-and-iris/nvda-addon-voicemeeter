from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self, controller, index):
        self._controller = controller
        self._index = index
        self._slider_mode = "gain"

    @abstractmethod
    def __str__(self):
        pass

    @property
    def identifier(self):
        return f"{self}[{self._index}]"

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val

    @property
    def slider_mode(self):
        return self._slider_mode

    @slider_mode.setter
    def slider_mode(self, val):
        self._slider_mode = val

    def get_bool(self, param: str) -> bool:
        return self._controller._get(f"{self.identifier}.{param}") == 1

    def set_bool(self, param: str, val: bool):
        self._controller._set(f"{self.identifier}.{param}", 1 if val else 0)

    def get_float(self, param: str) -> float:
        return round(self._controller._get(f"{self.identifier}.{param}"), 1)

    def set_float(self, param: str, val: float):
        self._controller._set(f"{self.identifier}.{param}", val)

    def get_int(self, param: str) -> int:
        return int(self._controller._get(f"{self.identifier}.{param}"))

    def set_int(self, param: str, val: int):
        self._controller._set(f"{self.identifier}.{param}", val)


class StripStrategy(Strategy):
    def __str__(self):
        return "Strip"


class BusStrategy(Strategy):
    def __str__(self):
        return "Bus"


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

    @property
    def slider_mode(self):
        return self._strategy._slider_mode

    @slider_mode.setter
    def slider_mode(self, val):
        self._strategy._slider_mode = val

    def get_bool(self, *args) -> bool:
        return self._strategy.get_bool(*args)

    def set_bool(self, *args):
        self._strategy.set_bool(*args)

    def get_float(self, *args) -> float:
        return self._strategy.get_float(*args)

    def set_float(self, *args):
        self._strategy.set_float(*args)

    def get_int(self, *args) -> int:
        return self._strategy.get_int(*args)

    def set_int(self, *args):
        self._strategy.set_int(*args)
