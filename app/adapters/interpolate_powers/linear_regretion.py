import numpy as np
from sklearn.linear_model import LinearRegression

from app.ports.interpolated_port import InterpolatePort


class LinearInterpolatePowers(InterpolatePort):
    """
    Class that trains a linear regression model to interpolate powers.

    Parameters
    ----------
    file_path : str
        Path to the csv file containing the data to train the model.

    Attributes
    ----------
    file_path : str
        Path to the csv file containing the data to train the model.
    model : object
        Linear Regression model object from sklearn.linear_model.
    _is_ready : bool
        Internal flag to check if the model is trained and ready for predictions.
    """

    def __init__(self, file_path: str = "app/adapters/interpolate_powers/data_set_brut.csv") -> None:
        self.file_path = file_path
        self.model = LinearRegression()
        self._is_ready = False

    def train(self):
        """
        Trains the model using the data from the file_path. Sets _is_ready to True after training.
        """
        data = self._extract_data()
        self._train_model(data)
        self._is_ready = True

    def _extract_data(self) -> np.ndarray:
        """
        Extracts the data from the csv file specified in file_path.

        Returns
        -------
        np.ndarray
            The data extracted from the csv file as a numpy array.
        """
        data = np.genfromtxt(self.file_path, delimiter=",", dtype=np.dtype(float))
        return data

    def _train_model(self, data: np.ndarray) -> None:
        """
        Trains the model using the provided data.

        Parameters
        ----------
        data : np.ndarray
            The data to train the model on.
        """
        X_train = data[:, :3]
        y_train = data[:, 3:]
        self.model.fit(X_train, y_train)

    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        """
        Predicts the result based on the given powers. The model must be trained before this method is called.

        Parameters
        ----------
        power_1 : float
            The first power.
        power_2 : float
            The second power.
        power_3 : float
            The third power.

        Returns
        -------
        np.ndarray
            The predicted result from the trained model as a 1D numpy array.

        Raises
        ------
        RuntimeError
            If the model is not trained before this method is called.
        """
        if not self._is_ready:
            raise RuntimeError("Model not ready. Please run the training process first.")
        actual_player = np.array([[power_1, power_2, power_3]])
        prediction = self.model.predict(actual_player)

        rounded_prediction = np.round(prediction).astype(int)

        # type [int, int, int, int]
        return rounded_prediction[0]


if __name__ == "__main__":
    interpolate = LinearInterpolatePowers("app/adapters/interpolate_powers/data_set.csv")
    interpolate.train()
    rep = interpolate.predicate(46521, 45308, 44142)
    print(rep)
