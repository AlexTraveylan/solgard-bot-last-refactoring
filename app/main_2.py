import datetime
import os

from dotenv import load_dotenv
from app.adapters.interpolate_powers.multi_regressor import MultiRegressor
from app.adapters.kuhn_munkres import KuhnMunkres
from app.adapters.print_assign_clash import PrintAssignClash
from app.adapters.string_assign_clash import AssignClashString
from app.adapters.traductor.translation import Translate
from app.core.models.bc_module import BCModule
from app.core.models.connect_user import ConnectUser
from app.core.models.get_guild import SetGuild
from app.core.models.player_2 import Player_2_data

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
KEY = os.getenv("KEY")
CONFIG_ENCRYPTED = os.getenv("CONFIG_ENCRYPTED")
if KEY is None:
    raise ValueError("KEY not found")
if CONFIG_ENCRYPTED is None:
    raise ValueError("CONFIG_ENCRYPTED not found")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")


def solo_for_t(context):
    allies_solo = context.values

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)

    play_2.allies_powersclash = [ally for ally in play_2.allies_powersclash if play_2.guild_members[ally.member_id] not in allies_solo]
    sorted_ennemies = sorted(play_2.ennemies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)
    ennemies_stronger = sorted_ennemies[: len(allies_solo)]
    play_2.ennemies_powersclash = sorted_ennemies[len(allies_solo) :]
    ennemies_name = [ennemi_guild_info.dict_members_id_name[ennemy.member_id] for ennemy in ennemies_stronger]
    solo_targets = [(f"{ally_solo} (solo mode)", ennemy) for ally_solo, ennemy in zip(allies_solo, ennemies_name)]

    trained_interpolate_module = MultiRegressor()
    trained_interpolate_module.train()
    bc_module = BCModule(play_2, ennemi_guild_info, trained_interpolate_module, Translate("fr"))

    kuhn_munkres = KuhnMunkres(*bc_module.get_tuple_for_kuhn_munkres())
    result_assign_list = kuhn_munkres.get_results()
    print_module = AssignClashString(result_assign_list)

    avantage = bc_module.get_avantage()
    targets_in_tuple_list = print_module.generate_allies_side_clash_strings()
    for field in [avantage, *solo_targets, *targets_in_tuple_list]:
        print(field)

    try:
        file_to_send = "app/adapters/tableau.png"
        file_path, ext = os.path.splitext(file_to_send)
        print_module = PrintAssignClash(result_assign_list)
        print_module.generate_table_image(file_path)

    except:
        print("Echec de la création du tableau en png")

    # os.remove(file_to_send)


if __name__ == "__main__":

    class Context:
        def __init__(self) -> None:
            self.values = ["Djoulz", "Miaou"]

    context = Context()
    solo_for_t(context)
