import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from app.ports.interpolated_port import InterpolatePort


class MultiRegressor(InterpolatePort):
    """
    Class that trains a multi-output random forest regression model to interpolate powers.

    Parameters
    ----------
    file_path : str
        Path to the csv file containing the data to train the model.

    Attributes
    ----------
    file_path : str
        Path to the csv file containing the data to train the model.
    model : object
        MultiOutputRegressor model object from sklearn.multioutput with RandomForestRegressor.
    _is_ready : bool
        Internal flag to check if the model is trained and ready for predictions.
    """

    def __init__(self, file_path: str = "app/adapters/interpolate_powers/data_set_brut.csv") -> None:
        self.file_path = file_path
        self.model = MultiOutputRegressor(RandomForestRegressor(random_state=42))
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

    def predicate(self, power_1: float, power_2: float, power_3: float) -> list[int]:
        """
        Predicts the result based on the given powers and adjusts the power levels.
        The model must be trained before this method is called.

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
        list[int]
            The adjusted predicted power levels as a list of integers.

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

        combined_results = [*actual_player[0], *rounded_prediction[0]]

        adjusted_results: list[int] = []
        for index, power in enumerate(combined_results):
            if power > combined_results[max(index - 1, 0)]:
                try:
                    adjusted_power = int((combined_results[index - 1] + combined_results[index + 1]) / 2)
                    adjusted_results.append(adjusted_power)
                except:
                    adjusted_power = combined_results[index - 1] - 2000
                    adjusted_results.append(adjusted_power)
            else:
                adjusted_results.append(power)

        return adjusted_results[3:]


if __name__ == "__main__":
    interpolate = MultiRegressor()
    interpolate.train()
    rep = interpolate.predicate(46521, 45308, 44142)
    print(rep)
