import pytest

from app.adapters.kuhn_munkres import AssignClash, KuhnMunkres
from app.core.models.bc_module import PowerTeam


@pytest.fixture
def mocked_kuhn_munkres():
    ennemies_team = [
        PowerTeam("a", 1, 40000),
        PowerTeam("a", 2, 35000),
        PowerTeam("a", 3, 27000),
        PowerTeam("b", 2, 42000),
        PowerTeam("b", 2, 37000),
        PowerTeam("b", 3, 30000),
    ]

    allies_team = [
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

    kuhn_munkres = KuhnMunkres(ennemies_team, allies_team)

    return kuhn_munkres


def test_integration_kuhn_munkres(mocked_kuhn_munkres):
    results: list[AssignClash] = mocked_kuhn_munkres.get_results()

    assert all([abs(result.ally_power - result.ennemy_power) <= 2500 for result in results])
