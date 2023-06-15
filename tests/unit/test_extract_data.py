import pytest
import numpy as np

from app.adapters.interpolate_powers.extract_data import InterpolatePowers


@pytest.fixture
def test_data():
    return "tests/data/data_set_test.csv"


def test_can_read_data(test_data):
    interpolate = InterpolatePowers(test_data)
    data = interpolate._extract_data()
    assert isinstance(data, np.ndarray)
    assert data.shape[1] == 7  # Assuming your data has 7 columns


def test_model_not_ready(test_data):
    interpolate = InterpolatePowers(test_data)
    with pytest.raises(RuntimeError):
        interpolate.predicate(1.0, 2.0, 3.0)


def test_can_train_model(test_data):
    interpolate = InterpolatePowers(test_data)
    interpolate.run()
    assert interpolate._is_ready


def test_can_predict(test_data):
    interpolate = InterpolatePowers(test_data)
    interpolate.run()
    prediction = interpolate.predicate(1.0, 2.0, 3.0)
    assert isinstance(prediction, np.ndarray)
    assert prediction.shape == (1, 4)  # Assuming your model predicts 4 outputs
