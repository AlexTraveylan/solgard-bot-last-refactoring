from discord.ext import commands
import discord
import os

BOT_KEY = os.getenv("BOT_KEY")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot command ready")


@bot.command("test")
async def test(context: commands.Context):
    await context.send("Test reussie avec succes")


bot.run(BOT_KEY)
