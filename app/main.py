import io
import time
from typing import Literal
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import datetime

from app.core.models.connect_user import ConnectUser
from app.core.models.player_2 import Player_2_data

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
print(time.tzname)


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
    await context.send(embed=embed)


@bot.command("connect_test")
async def connect_test(context: commands.Context):
    user = ConnectUser()
    user.connect_and_get_new_session_id()

    await context.send(f"```Connexion reussie :\nuser_id : {user.user_id}\nSession_id : {user.session_id}\n```")


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

    await context.send(response)


@bot.command("ab")
async def ab(context: commands.Context, nb_day: Literal[0, 1, 2, 3, 4, 5] = 0):
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())

    title = "Attaque(s) et bombe(s)"
    if nb_day == 0:
        description = "Attaques et bombes restantes de la journée"
    else:
        description = (
            f"Attaque(s) et bombe(s) manquante(s) {nb_day} jour(s) en arriere.\nJ'ai un bug non géré si vous demandez le mercredi de pause.\n"
        )

    now = datetime.datetime.now()
    colour = discord.Colour.blue()

    embed = discord.Embed(
        title=title,
        description=description,
        timestamp=now,
        colour=colour,
    )

    members = play_2.bombs_attacks.members_bomb_attacks
    members_missing_something = [
        member for member in members if (member.nb_attacks_used_by_day[nb_day] == 0 or member.nb_bomb_used_by_day[nb_day] == 0)
    ]

    for member in members_missing_something:
        member_name = play_2.guild_members[member.member_id]

        member_nb_atck = member.nb_attacks_used_by_day[nb_day]
        is_attack_done = member_nb_atck == 2
        if is_attack_done:
            display_atck = "Toutes les attaques effectués"
        else:
            display_atck = f"{2 - member_nb_atck} attaques restantes"

        member_nb_bomb = member.nb_bomb_used_by_day[nb_day]
        is_bomb_done = member_nb_bomb == 1
        if is_bomb_done:
            display_bomb = ""
        else:
            display_bomb = "Bombe non utilisée"
        embed.add_field(name=f"{member_name}", value=f"{display_atck}\n{display_bomb}", inline=False)

    await context.send(embed=embed)


bot.run(BOT_KEY)
