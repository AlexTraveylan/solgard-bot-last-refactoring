import os
from dotenv import load_dotenv
from naff import (
    Client,
    File,
    Intents,
    Button,
    ButtonStyles,
    ComponentContext,
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    component_callback,
    listen,
    slash_command,
    slash_option,
)

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
if BOT_KEY is None:
    raise ValueError("BOT_KEY not found")

bot = Client(intents=Intents.DEFAULT, auto_defer=True)


@listen()
async def on_startup():
    print(f"bot ready")


@slash_command(name="hello_world", description="My first command :)")
async def my_command(ctx: InteractionContext):
    """Says hello to the world"""

    # adds a component to the message
    components = Button(style=ButtonStyles.GREEN, label="Hiya", custom_id="hello_world_button")

    # adds an embed to the message
    embed = Embed(title="Hello World 2", description="Now extra fancy")

    # respond to the interaction
    await ctx.send("Hello World", embeds=embed, components=components)


@component_callback("hello_world_button")
async def my_callback(ctx: ComponentContext):
    """Callback for the component from the hello_world command"""

    await ctx.send("Hiya to you too")


@slash_command(name="file_test", description="file_test_command :)")
async def my_command_function(ctx: InteractionContext):
    file = File("app/adapters/tableau.png")
    await ctx.send("Hello World", file=file)


@slash_command(name="options_test", description="commande pour tester les options")
@slash_option(name="integer_option", description="Donne un nombre entier", required=True, opt_type=OptionTypes.INTEGER)
async def options_test(ctx: InteractionContext, integer_option: int):
    await ctx.send(f"Input : {integer_option}")


# start the bot
bot.start(BOT_KEY)
