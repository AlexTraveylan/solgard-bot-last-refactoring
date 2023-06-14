import io
from typing import Literal
import interactions

from dotenv import load_dotenv
import os
import datetime
from app.core.models.ab_module import ABModule
from app.core.models.b_module import BModule

from app.core.models.connect_user import ConnectUser
from app.core.models.get_guild import SetGuild
from app.core.models.info_clash_module import InfoClashModule, is_clash_on
from app.core.models.player_2 import Player_2_data

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")


class MainClient:
    def __init__(self) -> None:
        intents = interactions.Intents.ALL
        self.Client = interactions.Client(BOT_KEY, intents=intents)

    def start(self):
        self.Client.start()


interactions_client = MainClient()


@interactions_client.Client.event(name="on_ready")
async def on_ready():
    print("Bot command ready")


@interactions_client.Client.command(name="test", description="Do nothing, just a test")
async def test(context: interactions.CommandContext):
    return await context.send(f"`test reussi`")


@interactions_client.Client.command(name="connect_test", description="se connecte au jeu solgard")
async def connect_test(context: interactions.CommandContext):
    user = ConnectUser()
    user.connect_and_get_new_session_id()

    return await context.send(f"```Connexion reussie :\nuser_id : {user.user_id}\nSession_id : {user.session_id}\n```")


@interactions_client.Client.command(name="get_play_2", description="Recupere les données de player_2")
async def get_play_2(context: interactions.CommandContext):
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())

    message = io.StringIO()
    message.write("```Recupération de données :\n")
    message.write(f"Guild_id : {play_2.guild_id}\n")
    message.write(f"Guild_name : {play_2.guild_name}\n")
    message.write(f"Liste des {len(play_2.guild_members)} membres :\n")
    for member_id, member_name in play_2.guild_members.items():
        message.write(f"- {member_name} ({member_id})\n")
    message.write("```")

    response = message.getvalue()

    return await context.send(response)


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
    user = ConnectUser()
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
    user = ConnectUser()
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

    user = ConnectUser()
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


interactions_client.start()
