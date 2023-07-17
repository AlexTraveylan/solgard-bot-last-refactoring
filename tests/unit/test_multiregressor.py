import pytest
import numpy as np

from app.adapters.interpolate_powers.multi_regressor import MultiRegressor


@pytest.fixture
def test_data():
    return "tests/data/data_set_test.csv"


def test_can_read_data(test_data):
    interpolate = MultiRegressor(test_data)
    data = interpolate._extract_data()
    assert isinstance(data, np.ndarray)
    assert data.shape[1] == 7  # Assuming your data has 7 columns


def test_model_not_ready(test_data):
    interpolate = MultiRegressor(test_data)
    with pytest.raises(RuntimeError):
        interpolate.predicate(1.0, 2.0, 3.0)


def test_can_train_model(test_data):
    interpolate = MultiRegressor(test_data)
    interpolate.train()
    assert interpolate._is_ready


def test_can_predict(test_data):
    interpolate = MultiRegressor(test_data)
    interpolate.train()
    prediction = interpolate.predicate(1.0, 2.0, 3.0)
    assert isinstance(prediction, np.ndarray)
    assert prediction.shape == (4,)  # Assuming your model predicts 4 outputs
