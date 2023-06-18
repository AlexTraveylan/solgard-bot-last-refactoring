import io
from typing import Literal
import interactions

from dotenv import load_dotenv
import os
import datetime
from app.adapters.interpolate_powers.polynomial import PolynomialInterpolatePowers
from app.core.models.ab_module import ABModule
from app.core.models.b_module import BModule

from app.core.models.connect_user import ConnectUser
from app.core.models.get_guild import SetGuild
from app.core.models.info_clash_module import InfoClashModule, is_clash_on
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

    def start(self):
        self.Client.start()


interactions_client = MainClient()


@interactions_client.Client.command(
    name="ab",
    description="Renseigne les attaques et bombes restantes du jour, ou des jours précédents",
    options=[
        interactions.Option(
            type=interactions.OptionType.INTEGER,
            name="nb_day",
            description="Nombres de jours en arriere du recapitulatif",
            required=False,
        )
    ],
)
async def ab(context: interactions.CommandContext, nb_day: Literal[0, 1, 2, 3, 4] = 0):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ab_module = ABModule(play_2, nb_day)

    title = ab_module.title()
    description = ab_module.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, timestamp=now, color=3)

    fields_data = ab_module.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embeds=embed)


@interactions_client.Client.command(name="b", description="Donne le nombre de bombes restantes")
async def b(context: interactions.CommandContext):
    user = ConnectUser(CONFIG_ENCRYPTED, KEY)
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    b_module = BModule(play_2)

    title = b_module.title()
    description = b_module.description()
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    return await context.send(embeds=embed)


@interactions_client.Client.command(
    name="info_clash",
    description="Donne des infos sur le clash",
    options=[
        interactions.Option(
            type=interactions.OptionType.NUMBER,
            name="team_number",
            description="1 pour avoir les infos de l'équipe ennemie, par default : 0, notre équipe",
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
    info_clash = InfoClashModule(team_number, play_2, ennemi_guild_info)

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
    file_path = "app/adapters/interpolate_powers/data_set.csv"
    interpolate = PolynomialInterpolatePowers(file_path)
    interpolate.run()
    base = [power_1, power_2, power_3]
    result = interpolate.predicate(*base)

    title = "Prédiction des puissances"
    description = f"Puissances données :\n{base}\n\nPuissances prédites : \n{result[0]}"
    now = datetime.datetime.now()
    embed = interactions.Embed(title=title, description=description, color=5, timestamp=now)

    return await context.send(embeds=embed)


interactions_client.start()
