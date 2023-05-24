from discord.ext import commands
import discord
import os

from app.core.models.connect_user import ConnectUser

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
    await context.send("Test reussie avec succes")


@bot.command("connect_test")
async def connect_test(context: commands.Context):
    user = ConnectUser()
    user.connect()

    await context.send(f"```Connexion reussie :\nuser_id : {user.user_id}\nSession_id : {user.session_id}\n```")


bot.run(BOT_KEY)
