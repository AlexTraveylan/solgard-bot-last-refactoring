import numpy as np
from sklearn.linear_model import LinearRegression

from app.ports.interpolated_port import InterpolatePort


class LinearInterpolatePowers(InterpolatePort):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.model = LinearRegression()
        self._is_ready = False

    def train(self):
        """after this command, the model is trained then he can predicate"""
        data = self._extract_data()
        self._train_model(data)
        self._is_ready = True

    def _extract_data(self) -> np.ndarray:
        """read dataset"""
        data = np.genfromtxt(self.file_path, delimiter=",", dtype=np.dtype(float))
        return data

    def _train_model(self, data: np.ndarray) -> None:
        """train with dataset"""
        X_train = data[:, :3]
        y_train = data[:, 3:]
        self.model.fit(X_train, y_train)

    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        """train model before predicate"""
        if not self._is_ready:
            raise RuntimeError("Model not ready. Please run the training process first.")
        actual_player = np.array([[power_1, power_2, power_3]])
        prediction = self.model.predict(actual_player)

        rounded_prediction = np.round(prediction).astype(int)

        # type [[int, int, int, int]]
        return rounded_prediction
