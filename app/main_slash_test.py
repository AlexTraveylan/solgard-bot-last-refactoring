import os
from dotenv import load_dotenv
from interactions import Button, ButtonStyle, Client, Embed, File, Intents, OptionType, listen, slash_command, SlashContext, slash_option


load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")

bot = Client(intents=Intents.ALL)


@listen()
async def on_ready():
    print(f"bot ready")


@slash_command(name="hello_world", description="My first command :)")
async def my_command(ctx: SlashContext):
    """Says hello to the world"""

    # adds a component to the message
    components = Button(style=ButtonStyle.GREEN, label="Hiya", custom_id="hello_world_button")

    # adds an embed to the message
    embed = Embed(title="Hello World 2", description="Now extra fancy")

    # respond to the interaction
    await ctx.send("Hello World", embeds=embed, components=components)


@slash_command(name="file_test", description="file_test_command :)")
async def my_command_function(ctx: SlashContext):
    file = File("app/adapters/tableau.png")
    await ctx.send("Hello World", file=file)


@slash_command(name="options_test", description="commande pour tester les options")
@slash_option(name="integer_option", description="Donne un nombre entier", required=True, opt_type=OptionType.INTEGER)
async def options_test(ctx: SlashContext, integer_option: int):
    await ctx.send(f"Input : {integer_option}")


# start the bot
bot.start(BOT_KEY)
