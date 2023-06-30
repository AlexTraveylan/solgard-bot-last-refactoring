from typing import Literal
import interactions

from dotenv import load_dotenv
import os
import datetime
from app.adapters.date_time_fonctions import is_clash_on
from app.adapters.interpolate_powers.linear_regretion import LinearInterpolatePowers
from app.adapters.kuhn_munkres import KuhnMunkres
from app.adapters.string_assign_clash import AssignClashString
from app.adapters.traductor.translation import Translate
from app.core.models.ab_module import ABModule
from app.core.models.b_module import BModule
from app.core.models.bc_module import BCModule

from app.core.models.connect_user import ConnectUser
from app.core.models.get_guild import SetGuild
from app.core.models.info_clash_module import InfoClashModule
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


class MainClient:
    def __init__(self) -> None:
        intents = interactions.Intents.DEFAULT
        self.Client = interactions.Client(BOT_KEY, intents=intents)
        self.translate_module = Translate("fr")

    def start(self):
        self.Client.start()

    def change_langage(self, new_lang: Literal["fr", "en", "it", "es", "zh", "ru"]):
        self.translate_module.lang = new_lang
        self.translate_module.set_translation(new_lang)


interactions_client = MainClient()


@interactions_client.Client.command(
    name="ab",
    description="Fournit les informations sur les attaques et les bombes restantes du jour, ou des jours precedents",
    options=[
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="nb_day",
            description="Nombre de jours en arriere pour le recapitulatif",
            required=False,
        )
    ],
)
async def ab(context: interactions.CommandContext, nb_day: Literal[0, 1, 2, 3, 4] = 0):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ab_module = ABModule(play_2, nb_day, interactions_client.translate_module)

    title = ab_module.title()
    description = ab_module.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, timestamp=now, color=3)

    fields_data = ab_module.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


@interactions_client.Client.command(name="b", description="Fournit le nombre de bombes restantes")
async def b(context: interactions.CommandContext):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    b_module = BModule(play_2, interactions_client.translate_module)

    title = b_module.title()
    description = b_module.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    return await context.send(embeds=embed)


@interactions_client.Client.command(
    name="info_clash",
    description="Fournit des informations sur le clash",
    options=[
        interactions.Option(
            type=interactions.OptionType.NUMBER,
            name="team_number",
            description="1 pour obtenir les informations de l'equipe ennemie, par defaut : 0, notre equipe",
            required=False,
        )
    ],
)
async def infoClash(context: interactions.CommandContext, team_number: int = 0):
    now = datetime.datetime.utcnow()
    if not is_clash_on(now):
        return await context.send("`Pas de clash actif`")

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)
    info_clash = InfoClashModule(team_number, play_2, ennemi_guild_info, interactions_client.translate_module)

    title = info_clash.title()
    description = info_clash.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    fields_data = info_clash.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


@interactions_client.Client.command(
    name="power_interpolate",
    description="Utilise un modèle entrainé sur les données recoltées pour prédire les puissances suivantes.",
    options=[
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="power_1",
            description="Puissance de l'équipe 1, la plus puissante",
            required=True,
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="power_2",
            description="Puissance de l'équipe 2, la 2ème plus puissante",
            required=True,
        ),
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="power_3",
            description="Puissance de l'équipe 3, la 3ème plus puissante",
            required=True,
        ),
    ],
)
async def power_interpolate(context: interactions.CommandContext, power_1: int, power_2: int, power_3: int):
    file_path = "app/adapters/interpolate_powers/data_set_brut.csv"
    interpolate = LinearInterpolatePowers(file_path)
    interpolate.train()
    base = [power_1, power_2, power_3]
    result = interpolate.predicate(*base)

    title = "Prédiction des puissances"
    description = f"Puissances données :\n{base}\n\nPuissances prédites : \n{result}"
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    return await context.send(embeds=embed)


@interactions_client.Client.command(name="assign_clash_target", description="Cree les tableaux d'attribution pour le clash")
async def build_clash(context: interactions.CommandContext):
    now = datetime.datetime.utcnow()
    if not is_clash_on(now):
        return await context.send("`Pas de clash actif`")

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)
    trained_interpolate_module = LinearInterpolatePowers()
    trained_interpolate_module.train()
    bc_module = BCModule(play_2, ennemi_guild_info, trained_interpolate_module, interactions_client.translate_module)

    title = bc_module.title()
    description = bc_module.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    kuhn_munkres = KuhnMunkres(*bc_module.get_tuple_for_kuhn_munkres())
    result_assign_list = kuhn_munkres.get_results()
    print_module = AssignClashString(result_assign_list)

    fields_data = bc_module.embed_fields()
    avantage = bc_module.get_avantage()
    targets_in_tuple_list = print_module.generate_clash_strings()

    for field in [*fields_data, avantage, *targets_in_tuple_list]:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


@interactions_client.Client.command(
    name="set_langage",
    description="Permet de changer la langue du bot",
    options=[
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="langage",
            description="(1, francais) (2, english) (3, italiano) (4, spanish) (5, 中文) (6, русский)",
            required=True,
        )
    ],
)
async def set_langage(context: interactions.CommandContext, langage: Literal[1, 2, 3, 4, 5, 6]):
    if langage == 1:
        interactions_client.change_langage("fr")
        new_langage = "francais"
    elif langage == 2:
        interactions_client.change_langage("en")
        new_langage = "english"
    elif langage == 3:
        interactions_client.change_langage("it")
        new_langage = "italiano"
    elif langage == 4:
        interactions_client.change_langage("es")
        new_langage = "spanish"
    elif langage == 5:
        interactions_client.change_langage("zh")
        new_langage = "中文"
    elif langage == 6:
        interactions_client.change_langage("ru")
        new_langage = "русский"
    else:
        return await context.send(f"`{interactions_client.translate_module.translations['commands']['set_langage_command']['impossible_choice']}`")

    title = interactions_client.translate_module.translations["commands"]["set_langage_command"]["successful_change"]
    description = interactions_client.translate_module.translations["commands"]["set_langage_command"]["selected_language"].format(lang=new_langage)
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    return await context.send(embeds=embed)


interactions_client.start()
