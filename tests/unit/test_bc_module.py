import pytest
from unittest.mock import MagicMock, patch

from app.adapters.interpolate_powers.linear_regretion import LinearInterpolatePowers
from app.core.models.bc_module import BCModule
from app.core.models.get_guild import SetGuild
from app.core.models.player_2 import ClashTeam, Player_2_data, PowerClash


@pytest.fixture
def mocked_play_2():
    play_2 = MagicMock(spec=Player_2_data)
    play_2.ennemies_powersclash = [
        PowerClash(member_id="1", end_bonus=None, teams=[ClashTeam(45000, None, None), ClashTeam(43000, None, None), ClashTeam(42000, None, None)]),
        PowerClash(member_id="2", end_bonus=None, teams=[ClashTeam(48000, None, None), ClashTeam(47000, None, None), ClashTeam(46000, None, None)]),
    ]
    play_2.allies_powersclash = [
        PowerClash(member_id="10", end_bonus=None, teams=[ClashTeam(44500, None, None), ClashTeam(43500, None, None), ClashTeam(43000, None, None)]),
        PowerClash(member_id="20", end_bonus=None, teams=[ClashTeam(44500, None, None), ClashTeam(49500, None, None), ClashTeam(48500, None, None)]),
    ]
    play_2.guild_members = {
        "10": "fake_ally_1",
        "20": "fake_ally_2",
    }

    return play_2


@pytest.fixture
def mocked_ennemi_guild_info():
    ennemi_guild_info = MagicMock(spec=SetGuild)
    ennemi_guild_info.dict_members_id_name = {
        "1": "fake_ennemy_1",
        "2": "fake_ennemy_2",
    }

    return ennemi_guild_info


@pytest.fixture
def trained_interpolate_module():
    interpolate = LinearInterpolatePowers("tests/data/data_set_test.csv")
    interpolate.train()

    return interpolate


def test_BCModule__set_ennemies_powers_list(mocked_play_2, mocked_ennemi_guild_info, trained_interpolate_module):
    with patch.object(BCModule, "__init__", return_value=None):
        bc_module = BCModule()

    bc_module._play_2 = mocked_play_2
    bc_module._ennemi_guild_info = mocked_ennemi_guild_info
    bc_module._trained_interpolate_module = trained_interpolate_module

    tested_ennemies_powers_list = bc_module._set_ennemies_powers_list()

    assert len(tested_ennemies_powers_list) == 6
    assert tested_ennemies_powers_list[0].power == 45000
    assert tested_ennemies_powers_list[-1].power == 46000
    assert tested_ennemies_powers_list[0].member_name == "fake_ennemy_1"
    assert tested_ennemies_powers_list[-1].member_name == "fake_ennemy_2"


def test_BCModule__set_allies_powers_list(mocked_play_2, mocked_ennemi_guild_info, trained_interpolate_module):
    with patch.object(BCModule, "__init__", return_value=None):
        bc_module = BCModule()

    bc_module._play_2 = mocked_play_2
    bc_module._ennemi_guild_info = mocked_ennemi_guild_info
    bc_module._trained_interpolate_module = trained_interpolate_module

    tested_allies_powers_list = bc_module._set_allies_powers_list()

    assert len(tested_allies_powers_list) == 14
    assert all([10000 < ally.power < 50000 for ally in tested_allies_powers_list])
    assert tested_allies_powers_list[0].member_name == "fake_ally_1"
    assert tested_allies_powers_list[-1].member_name == "fake_ally_2"


def test_bc_module__set_total_powers(mocked_play_2):
    with patch.object(BCModule, "__init__", return_value=None):
        bc_module = BCModule()

    bc_module._play_2 = mocked_play_2

    ennemy_power_max, ally_power_max = bc_module._set_total_powers()

    assert ennemy_power_max == 271000
    assert ally_power_max == 273500
