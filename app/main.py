from typing import Literal
from interactions import (
    ActionRow,
    BrandColors,
    ButtonStyle,
    Client,
    File,
    Intents,
    Button,
    ComponentContext,
    Embed,
    InteractionContext,
    OptionType,
    StringSelectMenu,
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
from app.adapters.interpolate_powers.multi_regressor import MultiRegressor
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


@slash_command(name="ab", description="Provides information about the attacks and the remaining bombs of the current day or previous days.")
@slash_option(
    name="nb_day",
    description="Number of days back for the summary.",
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
    await context.defer()
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


@slash_command(name="b", description="Provides the number of remaining bombs.")
async def b(context: InteractionContext):
    await context.defer()
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    b_module = BModule(play_2, interactions_client.translate_module)

    title = b_module.title()
    description = b_module.description()
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.FUCHSIA, timestamp=now)

    return await context.send(embeds=embed)


@slash_command(name="info_clash", description="Provides information about the clash.")
@slash_option(
    name="team_number",
    description="Select the team for the rapport, default : Our team.",
    required=False,
    opt_type=OptionType.INTEGER,
    choices=[SlashCommandChoice(name="Our team", value=0), SlashCommandChoice(name="Their team", value=1)],
)
async def infoClash(context: InteractionContext, team_number: int = 0):
    await context.defer()
    now = datetime.datetime.utcnow()
    if not is_clash_on(now):
        return await context.send(interactions_client.translate_module.translations["assign_clash_target"]["clash_inactive"])

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


@slash_command(name="power_interpolate", description="Use machine learning module to show how it predict your powers.")
@slash_option(name="power_1", description="Your 1st defensive clash team.", required=True, opt_type=OptionType.INTEGER)
@slash_option(name="power_2", description="Your 2nd defensive clash team.", required=True, opt_type=OptionType.INTEGER)
@slash_option(name="power_3", description="Your 3rd defensive clash team.", required=True, opt_type=OptionType.INTEGER)
async def power_interpolate(context: InteractionContext, power_1: int, power_2: int, power_3: int):
    await context.defer()
    interpolate = MultiRegressor()
    interpolate.train()
    base = sorted([power_1, power_2, power_3], reverse=True)
    results = interpolate.predicate(*base)
    title = interactions_client.translate_module.translations["interpolate_module"]["title"]
    description = interactions_client.translate_module.translations["interpolate_module"]["description"].format(base=base, results=results)
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.GREEN, timestamp=now)

    return await context.send(embeds=embed)


@slash_command(name="set_langage", description="Allow you change the bot langage.")
@slash_option(
    name="langage",
    description="Select a langage.",
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
    await context.defer()
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
    description = interactions_client.translate_module.translations["commands"]["set_langage_command"]["selected_language"].format(
        lang=new_langage
    )
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.RED, timestamp=now)

    return await context.send(embeds=embed)


@slash_command(name="assign_clash_target", description="Assign target for the clash and publish it")
async def assign_clash_target(context: ComponentContext):
    await context.defer()

    now = datetime.datetime.utcnow()
    if not is_clash_on(now):
        return await context.send(interactions_client.translate_module.translations["assign_clash_target"]["clash_inactive"])

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    allies = sorted(list(play_2.guild_members.values()))

    components = StringSelectMenu(
        interactions_client.translate_module.translations["assign_clash_target"]["together"],
        *allies,
        placeholder=interactions_client.translate_module.translations["assign_clash_target"]["member_list"],
        min_values=1,
        max_values=len(allies),
        custom_id="solo_with_list",
    )
    await context.send(
        interactions_client.translate_module.translations["assign_clash_target"]["select_message"], components=components, ephemeral=True
    )


@component_callback("solo_with_list")
async def solo_with_list_callback(context: ComponentContext):
    await context.defer()
    allies_solo = context.values

    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ennemi_guild_info = SetGuild(user.user_id, user.session_id, play_2.clash_info.opponent_guild_id)

    if interactions_client.translate_module.translations["assign_clash_target"]["together"] not in allies_solo:
        sorted_allies = sorted(play_2.allies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)
        sorted_ennemies = sorted(play_2.ennemies_powersclash, key=lambda duels: sum([duel.power for duel in duels.teams]), reverse=True)
        solos_players_indexes = [index for index, ally in enumerate(sorted_allies) if play_2.guild_members[ally.member_id] in allies_solo]
        ennemies_solo_name = [ennemi_guild_info.dict_members_id_name[sorted_ennemies[index].member_id] for index in solos_players_indexes]
        allies_solo_name = [play_2.guild_members[sorted_allies[index].member_id] for index in solos_players_indexes]
        play_2.ennemies_powersclash = [ennemy for index, ennemy in enumerate(sorted_ennemies) if index not in solos_players_indexes]
        play_2.allies_powersclash = [ally for index, ally in enumerate(sorted_allies) if index not in solos_players_indexes]

        solo_targets = [(f"{ally_solo} (mode solo)", ennemy) for ally_solo, ennemy in zip(allies_solo_name, ennemies_solo_name)]
    else:
        solo_targets = []

    trained_interpolate_module = MultiRegressor()
    trained_interpolate_module.train()
    bc_module = BCModule(play_2, ennemi_guild_info, trained_interpolate_module, interactions_client.translate_module)

    title = bc_module.title()
    description = bc_module.description()
    now = datetime.datetime.now()
    embed = Embed(title=title, description=description, color=BrandColors.GREEN, timestamp=now)

    if len(play_2.allies_powersclash) > 0:
        kuhn_munkres = KuhnMunkres(*bc_module.get_tuple_for_kuhn_munkres())
        result_assign_list = kuhn_munkres.get_results()
        print_module = AssignClashString(result_assign_list)

        avantage = bc_module.get_avantage()
        targets_in_tuple_list = print_module.generate_allies_side_clash_strings()
        for field in [avantage, *solo_targets, *targets_in_tuple_list]:
            embed.add_field(name=field[0], value=field[1], inline=False)

        file_to_send = "app/adapters/tableau.png"
        file_path, ext = os.path.splitext(file_to_send)
        print_module = PrintAssignClash(result_assign_list)
        print_module.generate_table_image(file_path)

        await context.send(embeds=embed)

        file = File(file_to_send)
        await context.send(file=file)

        await context.delete(context.message_id)
        os.remove(file_to_send)

    else:
        for field in solo_targets:
            embed.add_field(name=field[0], value=field[1], inline=False)

        await context.send(embeds=embed)


@slash_command(name="version", description="Versions informations.")
async def version(context: ComponentContext):
    await context.defer()

    title = "Solgard bot -- version 1.0.0"
    description = "Free open source.\nDeveloped by AlexTraveylan.\nClic for see the repository."
    url = "https://github.com/AlexTraveylan/solgard-bot-last-refactoring"
    now = datetime.datetime.now()

    embed = Embed(title=title, description=description, url=url, timestamp=now, color=BrandColors.WHITE)

    await context.send(embeds=embed)


interactions_client.start()
