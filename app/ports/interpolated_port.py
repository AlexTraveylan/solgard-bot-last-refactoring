from abc import ABC, abstractmethod

import numpy as np


class InterpolatePort(ABC):
    @abstractmethod
    def train(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def predicate(self, **kwargs) -> np.ndarray:
        raise NotImplementedError
