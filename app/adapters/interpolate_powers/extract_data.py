import numpy as np
from sklearn.linear_model import LinearRegression


class InterpolatePowers:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.model = LinearRegression()
        self._is_ready = False

    def run(self):
        data = self._extract_data()
        self._train_model(data)
        self._is_ready = True

    def _extract_data(self) -> np.ndarray:
        data = np.genfromtxt(self.file_path, delimiter=",", dtype=np.dtype(float))
        return data

    def _train_model(self, data: np.ndarray) -> None:
        X_train = data[:, :3]
        y_train = data[:, 3:]
        self.model.fit(X_train, y_train)

    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        if not self._is_ready:
            raise RuntimeError("Model not ready. Please run the training process first.")
        actual_player = np.array([[power_1, power_2, power_3]])
        prediction = self.model.predict(actual_player)

        rounded_prediction = np.round(prediction).astype(int)

        return rounded_prediction


if __name__ == "__main__":
    file_path = "app/adapters/interpolate_powers/data_set.csv"

    interpolate = InterpolatePowers(file_path)
    interpolate.run()
    base = [44467, 43367, 40252]
    result = interpolate.predicate(*base)

    print([*base, *result[0]])
