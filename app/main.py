import io
import time
from typing import Literal
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import datetime
from app.adapters.date_time_fonctions import display_day_name_n_day_in_the_past
from app.core.models.ab_module import ABModule
from app.core.models.b_module import BModule

from app.core.models.connect_user import ConnectUser
from app.core.models.player_2 import Player_2_data

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot command ready")


@bot.command("test")
async def test(context: commands.Context):
    pass


@bot.command("connect_test")
async def connect_test(context: commands.Context):
    user = ConnectUser()
    user.connect_and_get_new_session_id()

    return await context.send(f"```Connexion reussie :\nuser_id : {user.user_id}\nSession_id : {user.session_id}\n```")


@bot.command("get_play_2")
async def get_play_2(context: commands.Context):
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


@bot.command("ab")
async def ab(context: commands.Context, nb_day: Literal[0, 1, 2, 3, 4] = 0):
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    ab_module = ABModule(play_2, nb_day)

    title = ab_module.title()
    description = ab_module.description()
    now = datetime.datetime.now()
    colour = discord.Colour.dark_blue()
    embed = discord.Embed(title=title, description=description, timestamp=now, colour=colour)

    fields_data = ab_module.embed_fields()
    for field in fields_data:
        embed.add_field(name=field[0], value=field[1], inline=False)

    return await context.send(embed=embed)


@bot.command("b")
async def b(context: commands.Context):
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    b_module = BModule(play_2)

    title = b_module.title()
    description = b_module.description()
    now = datetime.datetime.now()
    colour = discord.Colour.yellow()
    embed = discord.Embed(title=title, description=description, timestamp=now, colour=colour)

    return await context.send(embed=embed)


bot.run(BOT_KEY)
