from dataclasses import dataclass
from app.adapters.jsonreader import read_json

from app.core.models.get_guild import SetGuild
from app.core.models.info_clash_module import ClashStatut, InfoClashModule
from app.core.models.player_2 import ClashInfo, Player_2_data


@dataclass
class FakeSetGuild(SetGuild):
    def __post_init__(self):
        self.infos_guild = read_json("tests/data/reponse_viewguild_for_test.json")
        self._read_for_set_infos_guild()
        self._set_dict_members_id_name()


@dataclass
class FakePlayer_2_data(Player_2_data):
    def __post_init__(self):
        self.play_2_content = read_json("tests/data/reponse_play2_for_test.json")
        self._set_guild_infos()
        self.clash_info = ClashInfo(saison=1, id_clash="osef", opponent_guild_id="687c2b09-1889-47a9-836a-4fcd79373054", team_id=1)


def test_info_clash_module():
    play_2 = FakePlayer_2_data("user_id", "session_id")
    ennemi_guild_info = FakeSetGuild("user_id", "session_id", play_2.clash_info.opponent_guild_id)

    info_clash = InfoClashModule(1, play_2, ennemi_guild_info)

    assert len(info_clash.title()) > 10
    assert len(info_clash.total_dict) > 20
    assert info_clash.team == "team2"
    assert isinstance(info_clash.live_event_index, int)
    assert len(info_clash.clash_data) > 0
    assert len(info_clash.clash_members_statuts) > 0
    assert all([isinstance(data, ClashStatut) for data in info_clash.clash_members_statuts])
    assert len(info_clash.description()) > 10
    assert len(info_clash.embed_fields()) > 10
