import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from app.ports.interpolated_port import InterpolatePort


class PolynomialInterpolatePowers(InterpolatePort):
    """
    Class that trains a polynomial regression model to interpolate powers.

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
    transformer : object
        PolynomialFeatures object from sklearn.preprocessing.
    _is_ready : bool
        Internal flag to check if the model is trained and ready for predictions.
    """

    def __init__(self, file_path: str = "app/adapters/interpolate_powers/data_set_brut.csv") -> None:
        self.file_path = file_path
        self.model = LinearRegression()
        self.transformer = PolynomialFeatures(degree=2, include_bias=False)
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
        X_train_transformed = self.transformer.fit_transform(X_train)
        self.model.fit(X_train_transformed, y_train)

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
            The sorted, predicted result from the trained model as a 1D numpy array in descending order.

        Raises
        ------
        RuntimeError
            If the model is not trained before this method is called.
        """
        if not self._is_ready:
            raise RuntimeError("Model not ready. Please run the training process first.")
        actual_player = np.array([[power_1, power_2, power_3]])
        transformed_player = self.transformer.transform(actual_player)
        prediction = self.model.predict(transformed_player)

        rounded_prediction = np.round(prediction).astype(int)  # type [[int, int, int, int]]

        sorted_prediction = np.sort(rounded_prediction[0])[::-1]

        return sorted_prediction


if __name__ == "__main__":
    interpolate = PolynomialInterpolatePowers("app/adapters/interpolate_powers/data_set_brut.csv")
    interpolate.train()
    rep = interpolate.predicate(42244, 42165, 42148)
    print(rep)
