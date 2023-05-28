import io
import time
from typing import Literal
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
import datetime
from app.adapters.date_time_fonctions import display_day_name_n_day_in_the_past

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
async def ab(context: commands.Context, nb_day: Literal[0, 1, 2, 3, 4, 5] = 0):
    user = ConnectUser()
    user.connect_and_get_new_session_id()
    play_2 = Player_2_data(*user.get_user_id_session_id())
    members = play_2.bombs_attacks.members_bomb_attacks
    members_missing_something = [
        member for member in members if (member.nb_attacks_used_by_day[nb_day] == 0 or member.nb_bomb_used_by_day[nb_day] == 0)
    ]
    total_attacks_missing = sum([attacks.nb_attacks_used_by_day[nb_day] for attacks in members_missing_something])
    total_bombs_missing = sum([bombs.nb_bomb_used_by_day[nb_day] for bombs in members_missing_something])

    display_name_day = display_day_name_n_day_in_the_past(datetime.datetime.utcnow(), nb_day)

    title = f"Bilan pour {display_name_day}"
    if nb_day == 0:
        title = "Bilan actuel"
    else:
        title = f"Recapitulatif de {display_name_day}"
    if nb_day == 0:
        if total_attacks_missing + total_bombs_missing == 0:
            description = "Toutes les attaques et les bombes ont été utilisées, bravo a tous."
        else:
            description = f"Attaques et bombes restantes du jour.\nIl reste :\n- {total_attacks_missing} attaques\n- {total_bombs_missing} bombes"
    else:
        description = f"Demande d'un recapitulatif des attaque(s) et bombe(s) manquante(s) {nb_day} jour(s) dans le passé.\nDemande faite par {context.author.mention}\n"
        description += f"Attaques et bombes oubliées :\n- {total_attacks_missing} attaques\n- {total_bombs_missing} bombes"

    now = datetime.datetime.now()
    colour = discord.Colour.dark_blue()
    color = discord.Color.dark_magenta()

    embed = discord.Embed(title=title, description=description, timestamp=now, colour=colour, color=color)

    is_rest_day = len(members_missing_something) == len(members)
    if is_rest_day:
        embed.description = "Aucune attaque et bombe un jour de repos"
        return await context.send(embed=embed)

    for member in members_missing_something:
        member_name = play_2.guild_members[member.member_id]

        member_nb_atck = member.nb_attacks_used_by_day[nb_day]
        is_attack_done = member_nb_atck == 2
        if is_attack_done:
            display_atck = ""
        else:
            remaining_attacks = 2 - member_nb_atck
            display_atck = f"{':crossed_swords:' * remaining_attacks}  {remaining_attacks} attaques restantes\n"

        member_nb_bomb = member.nb_bomb_used_by_day[nb_day]
        is_bomb_done = member_nb_bomb == 1
        if is_bomb_done:
            display_bomb = ""
        else:
            display_bomb = ":bomb:  Bombe non utilisée"
        embed.add_field(name=f"{member_name}", value=f"{display_atck}{display_bomb}\n", inline=False)

    return await context.send(embed=embed)


bot.run(BOT_KEY)
