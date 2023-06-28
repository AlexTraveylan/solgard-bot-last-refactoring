from app.core.models.bc_module import PowerTeam
import pytest
from unittest.mock import MagicMock, patch
from app.adapters.kuhn_munkres import KuhnMunkres


@pytest.fixture
def mocked_kuhn_munkres():
    with patch.object(KuhnMunkres, "__init__", return_value=None):
        kuhn_munkres = KuhnMunkres(None, None)

    kuhn_munkres.ennemies_team = [
        PowerTeam("a", 1, 40000),
        PowerTeam("a", 2, 35000),
        PowerTeam("a", 3, 27000),
        PowerTeam("b", 2, 42000),
        PowerTeam("b", 2, 37000),
        PowerTeam("b", 3, 30000),
    ]

    kuhn_munkres.allies_team = [
        PowerTeam("c", 1, 26500),
        PowerTeam("c", 2, 36500),
        PowerTeam("c", 3, 29500),
        PowerTeam("c", 4, 41500),
        PowerTeam("c", 5, 25500),
        PowerTeam("d", 1, 53500),
        PowerTeam("d", 2, 41500),
        PowerTeam("d", 3, 31500),
        PowerTeam("d", 4, 32500),
        PowerTeam("d", 5, 28500),
    ]

    kuhn_munkres._allies_powers = [25000, 30000, 35000]

    kuhn_munkres._ennemies_powers = [27500, 29500, 32500, 33500, 37500]

    return kuhn_munkres


def test_split_name_powers_with_allies(mocked_kuhn_munkres):
    names, powers = mocked_kuhn_munkres._split_name_powers("ally")

    assert names[0] == ("c", 1)
    assert powers[0] == 26500
    assert names[-1] == ("d", 5)
    assert powers[-1] == 28500


def test_split_name_powers_with_ennemies(mocked_kuhn_munkres):
    names, powers = mocked_kuhn_munkres._split_name_powers("ennemy")

    assert names[0] == ("a", 1)
    assert powers[0] == 40000
    assert names[-1] == ("b", 3)
    assert powers[-1] == 30000


def test_create_cost_matrix(mocked_kuhn_munkres):
    cost_matrix = mocked_kuhn_munkres._create_cost_matrix()

    assert cost_matrix.shape == (5, 3)
