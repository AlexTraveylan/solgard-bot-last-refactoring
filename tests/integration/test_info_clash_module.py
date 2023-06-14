from dataclasses import dataclass
import datetime
from app.adapters.jsonreader import read_json

from app.core.models.get_guild import SetGuild
from app.core.models.info_clash_module import ClashStatut, InfoClashModule, is_clash_on
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


def test_is_clash_on_weekend():
    now = datetime.datetime(2023, 6, 16, 15, 0)  # Vendredi après 14h UTC
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 12, 0)  # Samedi
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 14, 0)  # Samedi après 14h UTC
    assert is_clash_on(now) == True


def test_is_clash_on_weekday():
    now = datetime.datetime(2023, 6, 15, 10, 0)  # Jeudi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 16, 10, 0)  # Vendredi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 18, 15, 0)  # Dimanche après 14h UTC
    assert is_clash_on(now) == False


def test_is_clash_on_edge_cases():
    now = datetime.datetime(2023, 6, 14, 14, 0)  # Mardi avant 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 20, 14, 0)  # Lundi après 14h UTC
    assert is_clash_on(now) == False

    now = datetime.datetime(2023, 6, 17, 13, 0)  # Samedi avant 14h UTC
    assert is_clash_on(now) == True

    now = datetime.datetime(2023, 6, 17, 14, 0)  # Samedi après 14h UTC
    assert is_clash_on(now) == True
