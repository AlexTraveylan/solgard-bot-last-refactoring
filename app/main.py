from typing import Literal
from interactions import (
    BrandColors,
    Client,
    Color,
    File,
    Intents,
    Button,
    ComponentContext,
    Embed,
    Extension,
    InteractionContext,
    OptionType,
    component_callback,
    listen,
    slash_command,
    slash_option,
    SlashCommandChoice,
)

from dotenv import load_dotenv
import os
import datetime
from app.adapters.date_time_fonctions import is_clash_on
from app.adapters.interpolate_powers.linear_regretion import LinearInterpolatePowers
from app.adapters.kuhn_munkres import KuhnMunkres
from app.adapters.print_assign_clash import PrintAssignClash
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
        self.bot = Client(intents=Intents.ALL, auto_defer=True)
        self.translate_module = Translate("fr")

    def start(self):
        self.bot.start(BOT_KEY)

    def change_langage(self, new_lang: Literal["fr", "en", "it", "es", "zh", "ru"]):
        self.translate_module.lang = new_lang
        self.translate_module.set_translation(new_lang)


interactions_client = MainClient()


@listen()
async def on_startup():
    print(f"Bot ready")


@slash_command(name="ab", description="Fournit les informations sur les attaques et les bombes restantes du jour, ou des jours precedents")
@slash_option(
    name="nb_day",
    description="Nombre de jours en arriere pour le recapitulatif",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice(name="Today", value=0),
        SlashCommandChoice(name="Yesterday", value=1),
        SlashCommandChoice(name="Two days", value=2),
        SlashCommandChoice(name="Tree days", value=3),
        SlashCommandChoice(name="Four days", value=4),
    ],
)
async def ab(context: InteractionContext, nb_day: Literal[0, 1, 2, 3, 4] = 0):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ab_module = ABModule(play_2, nb_day, interactions_client.translate_module)

    title = ab_module.title()
    description = ab_module.description()
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, timestamp=now, color=BrandColors.BLURPLE)

    fields_data = ab_module.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


@slash_command(name="b", description="Fournit le nombre de bombes restantes")
async def b(context: InteractionContext):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    b_module = BModule(play_2, interactions_client.translate_module)

    title = b_module.title()
    description = b_module.description()
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.FUCHSIA, timestamp=now)

    return await context.send(embeds=embed)


@slash_command(name="info_clash", description="Fournit des informations sur le clash")
@slash_option(
    name="team_number",
    description="Choix de la team concerné par le report",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[SlashCommandChoice(name="Our team", value=0), SlashCommandChoice(name="Their team", value=1)],
)
async def infoClash(context: InteractionContext, team_number: int = 0):
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
    embed = Embed(title=title, description=description, color=BrandColors.RED, timestamp=now)

    fields_data = info_clash.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


# @interactions_client.Client.command(
#     name="power_interpolate",
#     description="Utilise un modèle entrainé sur les données recoltées pour prédire les puissances suivantes.",
#     options=[
#         interactions.Option(
#             type=interactions.OptionType.INTEGER,
#             name="power_1",
#             description="Puissance de l'équipe 1, la plus puissante",
#             required=True,
#         ),
#         interactions.Option(
#             type=interactions.OptionType.INTEGER,
#             name="power_2",
#             description="Puissance de l'équipe 2, la 2ème plus puissante",
#             required=True,
#         ),
#         interactions.Option(
#             type=interactions.OptionType.INTEGER,
#             name="power_3",
#             description="Puissance de l'équipe 3, la 3ème plus puissante",
#             required=True,
#         ),
#     ],
# )
# async def power_interpolate(context: interactions.CommandContext, power_1: int, power_2: int, power_3: int):
#     file_path = "app/adapters/interpolate_powers/data_set_brut.csv"
#     interpolate = LinearInterpolatePowers(file_path)
#     interpolate.train()
#     base = [power_1, power_2, power_3]
#     result = interpolate.predicate(*base)

#     title = "Prédiction des puissances"
#     description = f"Puissances données :\n{base}\n\nPuissances prédites : \n{result}"
#     now = datetime.datetime.now()
#     embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

#     return await context.send(embeds=embed)


@slash_command(name="assign_clash_target", description="Cree les tableaux d'attribution pour le clash")
@slash_option(name="is_allies_side", description="Point de vue allié ?", required=False, opt_type=OptionType.BOOLEAN)
async def build_clash(context: InteractionContext, is_allies_side: bool = True):
    now = datetime.datetime.utcnow()
    if not is_clash_on(now):
        return await context.send("`Pas de clash actif`")

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)

    play_2.allies_powersclash = [ally for ally in play_2.allies_powersclash if play_2.guild_members[ally.member_id] != "Djoulz"]
    sorted_ennemies = sorted(play_2.ennemies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)
    ennemy_stronger = sorted_ennemies[0]
    play_2.ennemies_powersclash = sorted_ennemies[1:]
    try:
        ennemy_name = ennemi_guild_info.dict_members_id_name[ennemy_stronger.member_id]
    except KeyError:
        ennemy_name = "Trouve toi même l'ennemi manquant, sorry ca a fail"
    djoulz_target = "Djoulz (mode solo)", f"{ennemy_name}"

    trained_interpolate_module = LinearInterpolatePowers()
    trained_interpolate_module.train()
    bc_module = BCModule(play_2, ennemi_guild_info, trained_interpolate_module, interactions_client.translate_module)

    title = bc_module.title()
    description = bc_module.description()
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.GREEN, timestamp=now)

    kuhn_munkres = KuhnMunkres(*bc_module.get_tuple_for_kuhn_munkres())
    result_assign_list = kuhn_munkres.get_results()
    print_module = AssignClashString(result_assign_list)

    fields_data = bc_module.embed_fields()
    avantage = bc_module.get_avantage()
    if is_allies_side:
        targets_in_tuple_list = print_module.generate_allies_side_clash_strings()
    else:
        targets_in_tuple_list = print_module.generate_clash_strings()
    for field in [*fields_data, avantage, djoulz_target, *targets_in_tuple_list]:
        embed.add_field(name=field[0], value=field[1], inline=False)

    file_to_send = "app/adapters/tableau.png"
    file_path, ext = os.path.splitext(file_to_send)
    print_module = PrintAssignClash(result_assign_list)
    print_module.generate_table_image(file_path)

    file = File(file_to_send)

    await context.send(embeds=embed, file=file)

    os.remove(file_to_send)


@slash_command(name="set_langage", description="Permet de changer la langue du bot")
@slash_option(
    name="langage",
    description="Nombre de jours en arriere pour le recapitulatif",
    required=True,
    opt_type=OptionType.INTEGER,
    choices=[
        SlashCommandChoice(name="francais", value=1),
        SlashCommandChoice(name="english", value=2),
        SlashCommandChoice(name="italiano", value=3),
        SlashCommandChoice(name="spanish", value=4),
        SlashCommandChoice(name="中文", value=5),
        SlashCommandChoice(name="русский", value=6),
    ],
)
async def set_langage(context: InteractionContext, langage: Literal[1, 2, 3, 4, 5, 6]):
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
    embed = Embed(title=title, description=description, color=BrandColors.RED, timestamp=now)

    return await context.send(embeds=embed)


# @interactions_client.Client.command(name="test4", description="test button")
# async def test4(context: interactions.CommandContext):
#     choix = interactions.Button(
#         style=interactions.ButtonStyle.DANGER,
#         label="ping",
#         custom_id="send_ping",
#     )

#     choix2 = interactions.Button(
#         style=interactions.ButtonStyle.SUCCESS,
#         label="pong",
#         custom_id="send_pong",
#     )

#     action_row = interactions.ActionRow(components=[choix, choix2])

#     return await context.send("Cliquez sur le bouton pour envoyer un ping", components=action_row, ephemeral=True)


# @interactions_client.Client.command(name="test_menu", description="test les le selectMenu")
# async def test3(context: interactions.CommandContext):
#     select_menu = interactions.SelectMenu(
#         custom_id="select_menu",
#         options=[
#             interactions.SelectOption(label="francais", value="fr"),
#             interactions.SelectOption(label="english", value="en"),
#             interactions.SelectOption(label="italiano", value="it"),
#             interactions.SelectOption(label="spanish", value="es"),
#             interactions.SelectOption(label="中文", value="zh"),
#             interactions.SelectOption(label="русский", value="ru"),
#         ],
#         placeholder="Select a langage",
#     )

#     await context.send("Choose a langage", components=select_menu, ephemeral=True)


# @interactions_client.Client.component("send_ping")
# @interactions_client.Client.component("send_pong")
# async def danger_component(context: interactions.CommandContext):
#     return await context.send(context.data.custom_id)


# @interactions_client.Client.component("select_menu")
# async def select_menu_component(context: interactions.ComponentContext, values: list[str]):
#     embed = interactions.Embed(title="Changement réussi", description=f"nouveau langage : {values[0]}", color=555555)

#     await context.edit(content="", embeds=embed, components=[])


# @interactions_client.Client.command(name="test_embed_file", description="test_embed_file")
# async def test_embed_file(context: interactions.CommandContext):
#     print(type(context))
#     embed = interactions.Embed(title="titre_test", description="description_test", color=77777)
#     file = interactions.File("app/adapters/tableau.png")

#     await context.send(file=file)


interactions_client.start()
