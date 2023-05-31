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
    now = datetime.datetime.now()
    colour = discord.Colour.blue()
    embed = discord.Embed(
        title="Test embed de test",
        color=discord.Color.yellow(),
        description="Alors, blabla blablabla blabalblabalblabla. Voila\nThe end.",
        timestamp=now,
        type="image",
        colour=colour,
        url="https://img.freepik.com/photos-premium/image-galaxie-coloree-dans-ciel-ai-generative_791316-9864.jpg?w=2000",
    )
    embed.set_image(url="https://img.freepik.com/photos-premium/image-galaxie-coloree-dans-ciel-ai-generative_791316-9864.jpg?w=2000")
    embed.add_field(name="2eme champ", value="contenu du 2eme champ")
    embed.add_field(name="fuseau horaire", value=f"{time.tzname}")
    return await context.send(embed=embed)


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
    members = play_2.bombs_attacks.members_bomb_attacks
    members_missing_something = [member for member in members if member.nb_bomb_used_by_day[0] == 0]
    total_bombs_missing = len(members_missing_something)

    title = "Bombes restantes aujourd'hui."
    description_io = io.StringIO()

    now = datetime.datetime.now()
    colour = discord.Colour.yellow()

    embed = discord.Embed(title=title, description="description", timestamp=now, colour=colour)

    if total_bombs_missing == 0:
        description_io.write("Toutes les bombes ont été utilisées.\n")
        embed.description = description_io.getvalue()
        return await context.send(embed=embed)
    else:
        description_io.write(f"Il reste {total_bombs_missing} bombes non utilisées.\n")

    for member in members_missing_something:
        member_name = play_2.guild_members[member.member_id]
        description_io.write(f":bomb:  {member_name}\n")

    embed.description = description_io.getvalue()
    return await context.send(embed=embed)


bot.run(BOT_KEY)
