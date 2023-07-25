from abc import ABC, abstractmethod

import numpy as np


class InterpolatePort(ABC):
    """
    An abstract base class for interpolation. This class provides the structure for creating subclasses for
    different interpolation techniques.

    Attributes
    ----------
    _is_ready : bool
        A private variable that indicates whether the model is ready for prediction.
    """

    _is_ready: bool

    @abstractmethod
    def train(self) -> None:
        """
        Abstract method that should be implemented in subclass to train the interpolation model.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        """
        Abstract method that should be implemented in subclass to predict the interpolation value based on the input powers.

        Parameters
        ----------
        power_1 : float
            The first power input.
        power_2 : float
            The second power input.
        power_3 : float
            The third power input.

        Returns
        -------
        np.ndarray
            The predicted interpolation value(s).

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        raise NotImplementedError
