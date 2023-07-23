from app.adapters.jsonreader import read_json
from app.core.models.player_2 import Player_2_data
from unittest.mock import patch


FILE_PATH = "tests/data/reponse_play2_for_test.json"


def test_build_clash():
    with patch.object(Player_2_data, "__post_init__", return_value=None):
        player_2 = Player_2_data(user_id="fake_user", session_id="fake_session_id")

    data = read_json(FILE_PATH)

    player_2.play_2_content = data

    player_2._set_clash_info()
    player_2._set_clash_event()
    player_2.ennemies_powersclash = player_2._get_clash_power("ennemy")
    player_2.allies_powersclash = player_2._get_clash_power("ally")

    allies_solo = ["Djoulz", "Miaou"]

    # ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)

    # play_2.allies_powersclash = [ally for ally in play_2.allies_powersclash if play_2.guild_members[ally.member_id] not in allies_solo]
    # sorted_ennemies = sorted(play_2.ennemies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)
    # ennemies_stronger = sorted_ennemies[: len(allies_solo)]
    # play_2.ennemies_powersclash = sorted_ennemies[len(allies_solo) :]
    # ennemies_name = [ennemi_guild_info.dict_members_id_name[ennemy.member_id] for ennemy in ennemies_stronger]
    # solo_targets = [(f"{ally_solo} (solo mode)", ennemy) for ally_solo, ennemy in zip(allies_solo, ennemies_name)]

    # trained_interpolate_module = MultiRegressor()
    # trained_interpolate_module.train()
    # bc_module = BCModule(play_2, ennemi_guild_info, trained_interpolate_module, Translate("fr"))

    # kuhn_munkres = KuhnMunkres(*bc_module.get_tuple_for_kuhn_munkres())
    # result_assign_list = kuhn_munkres.get_results()
    # print_module = AssignClashString(result_assign_list)

    # avantage = bc_module.get_avantage()
    # targets_in_tuple_list = print_module.generate_allies_side_clash_strings()
    # for field in [avantage, *solo_targets, *targets_in_tuple_list]:
    #     print(field)

    # try:
    #     file_to_send = "app/adapters/tableau.png"
    #     file_path, ext = os.path.splitext(file_to_send)
    #     print_module = PrintAssignClash(result_assign_list)
    #     print_module.generate_table_image(file_path)

    # except:
    #     print("Echec de la création du tableau en png")

    # os.remove(file_to_send)
