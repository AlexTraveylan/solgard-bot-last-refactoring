from dataclasses import dataclass

import pytest
from app.adapters.jsonreader import read_json

from app.core.models.get_guild import Member, SetGuild


@dataclass
class FakeSetGuild(SetGuild):
    def __post_init__(self):
        self.infos_guild = read_json("tests/data/reponse_viewguild_for_test.json")


def test_read_for_set_infos_guild():
    set_guild = FakeSetGuild(user_id="fake_id", session_id="fake_sid", guild_id="fake_gid")

    set_guild._read_for_set_infos_guild()

    assert len(set_guild.members) == 20
    assert all(isinstance(member, Member) for member in set_guild.members)


def test__set_dict_members_id_name():
    set_guild = FakeSetGuild(user_id="fake_id", session_id="fake_sid", guild_id="fake_gid")

    member_1 = Member("1", "a", True)
    member_2 = Member("2", "b", False)
    set_guild.members = [member_1, member_2]

    set_guild._set_dict_members_id_name()

    assert set_guild.dict_members_id_name["1"] == "a"
    assert set_guild.dict_members_id_name["2"] == "b"

    with pytest.raises(KeyError):
        set_guild.dict_members_id_name["3"]
