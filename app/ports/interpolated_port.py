from abc import ABC, abstractmethod

import numpy as np


class InterpolatePort(ABC):
    _is_ready: bool

    @abstractmethod
    def train(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        raise NotImplementedError
