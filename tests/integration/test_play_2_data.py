from app.core.models.connect_user import ConnectUser
from app.core.models.player_2 import Player_2_data


def test_player_2_data():
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    user_infos = user.get_user_id_session_id()
    player_2_data = Player_2_data(*user_infos)

    assert player_2_data.guild_id is not None
    assert player_2_data.guild_name is not None
    assert player_2_data.play_2_content is not None
    assert player_2_data.guild_members is not None
    assert 1 < len(player_2_data.guild_members) <= 20
