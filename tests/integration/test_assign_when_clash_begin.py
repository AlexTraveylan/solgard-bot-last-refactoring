from app.adapters.jsonreader import read_json
from app.core.models.player_2 import Player_2_data
from unittest.mock import patch


FILE_PATH = "tests/data/reponse_play2_for_test.json"


def test_recup_powers_when_clash_is_begin():
    with patch.object(Player_2_data, "__post_init__", return_value=None):
        player_2 = Player_2_data(user_id="fake_user", session_id="fake_session_id")

    data = read_json(FILE_PATH)

    player_2.play_2_content = data

    player_2._set_clash_info()
    player_2._set_clash_event()
    player_2.ennemies_powersclash = player_2._get_clash_power("ennemy")
    player_2.allies_powersclash = player_2._get_clash_power("ally")

    assert all([len(ennemy.teams) == 3 for ennemy in player_2.ennemies_powersclash])
    assert all([len(ally.teams) == 3 for ally in player_2.allies_powersclash])
