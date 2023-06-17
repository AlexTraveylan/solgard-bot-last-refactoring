import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from app.ports.interpolated_port import InterpolatePort


class PolynomialInterpolatePowers(InterpolatePort):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.model = LinearRegression()
        self.transformer = PolynomialFeatures(degree=2, include_bias=False)
        self._is_ready = False

    def train(self):
        data = self._extract_data()
        self._train_model(data)
        self._is_ready = True

    def _extract_data(self) -> np.ndarray:
        data = np.genfromtxt(self.file_path, delimiter=",", dtype=np.dtype(float))
        return data

    def _train_model(self, data: np.ndarray) -> None:
        X_train = data[:, :3]
        y_train = data[:, 3:]
        X_train_transformed = self.transformer.fit_transform(X_train)
        self.model.fit(X_train_transformed, y_train)

    def predicate(self, power_1: float, power_2: float, power_3: float) -> np.ndarray:
        if not self._is_ready:
            raise RuntimeError("Model not ready. Please run the training process first.")
        actual_player = np.array([[power_1, power_2, power_3]])
        transformed_player = self.transformer.transform(actual_player)
        prediction = self.model.predict(transformed_player)

        rounded_prediction = np.round(prediction).astype(int)  # type [[int, int, int, int]]

        sorted_prediction = np.sort(rounded_prediction[0])[::-1]

        return sorted_prediction


if __name__ == "__main__":
    interpolate = PolynomialInterpolatePowers("app/adapters/interpolate_powers/data_set.csv")
    interpolate.train()
    rep = interpolate.predicate(49859, 47492, 45760)
    print(rep)
