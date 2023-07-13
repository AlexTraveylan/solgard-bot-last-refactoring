from unittest.mock import MagicMock

from app.core.models.player_2 import ClashTeam, Player_2_data, PowerClash


def test_mode_solo():
    play_2 = MagicMock(spec=Player_2_data)
    play_2.ennemies_powersclash = [
        PowerClash(member_id="1", end_bonus=None, teams=[ClashTeam(45000, None, None), ClashTeam(43000, None, None), ClashTeam(42000, None, None)]),
        PowerClash(member_id="2", end_bonus=None, teams=[ClashTeam(48000, None, None), ClashTeam(47000, None, None), ClashTeam(46000, None, None)]),
        PowerClash(member_id="3", end_bonus=None, teams=[ClashTeam(70000, None, None), ClashTeam(80000, None, None), ClashTeam(90000, None, None)]),
    ]
    play_2.allies_powersclash = [
        PowerClash(member_id="10", end_bonus=None, teams=[ClashTeam(44500, None, None), ClashTeam(43500, None, None), ClashTeam(43000, None, None)]),
        PowerClash(member_id="20", end_bonus=None, teams=[ClashTeam(44500, None, None), ClashTeam(49500, None, None), ClashTeam(48500, None, None)]),
        PowerClash(member_id="30", end_bonus=None, teams=[ClashTeam(44500, None, None), ClashTeam(49500, None, None), ClashTeam(48500, None, None)]),
    ]
    play_2.guild_members = {
        "10": "Djoulz",
        "20": "fake_ally_2",
        "30": "fake_ally_3",
    }

    Player_2_data.allies_powersclash = []

    play_2.allies_powersclash = [ally for ally in play_2.allies_powersclash if play_2.guild_members[ally.member_id] != "Djoulz"]
    play_2.ennemies_powersclash = sorted(play_2.ennemies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)[1:]

    assert len(play_2.allies_powersclash) == 2
    assert all([ally.member_id != "10" for ally in play_2.allies_powersclash])

    assert len(play_2.ennemies_powersclash) == 2
    assert all([ennemy.member_id != "3" for ennemy in play_2.ennemies_powersclash])
