import pytest
from app.core.models.player_2 import BombsAttacks, MemberBombAttacks


def test_bomb_attacks_find_existing_member():
    member_1 = MemberBombAttacks("1", {}, {})
    member_2 = MemberBombAttacks("2", {}, {})

    bombattacks = BombsAttacks([member_1, member_2])
    searched_member = bombattacks.find_member_by_member_id("1")

    assert isinstance(searched_member, MemberBombAttacks)


def test_bomb_attacks_not_founded_member_raise_value_error():
    member_1 = MemberBombAttacks("1", {}, {})
    member_2 = MemberBombAttacks("2", {}, {})

    bombattacks = BombsAttacks([member_1, member_2])

    with pytest.raises(ValueError):
        bombattacks.find_member_by_member_id("3")
