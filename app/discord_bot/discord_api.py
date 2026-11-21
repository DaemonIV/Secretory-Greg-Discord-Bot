from dotenv import load_dotenv
import discord
import os
from app.chatgpt_ai.ai_client import chatgpt_response
from app.player_cards.PlayerCardsGreg import generate_player_card

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True



bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------------------------------')
    print("C")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)
    


@bot.slash_command(name="rules", description="Get the rules of the server")
async def rules(ctx: discord.ApplicationContext, prompt: discord.Option(str, "Enter your questions about the rules of the server")):
    print(prompt)
    await ctx.defer()
    bot_response = chatgpt_response(prompt=prompt)
    await ctx.respond(f"{bot_response}")

STAT_CHOICES = [
    "Final Kills", "Kills", "Average Kills per season", "Worst placement",
    "Best placement", "Average placement", "Chaos Life", "Chaos Life^2",
]

BACKGROUND_CHOICES = [
    "Enchanted Warped Forest", "Bloody Crimson", "Mooshroom Isles",
    "Grand Canyon", "Distant Horizons", "Dappled Hills",
    "Mountain's Peak", "Cherry Mountains", "Skeleton Meadows", "Pale Highlands",
]

POSE_CHOICES = [
    "Default", "Marching", "Crouching", "Crossed", "Criss-cross", "Ultimate", "Isometric", "Head", " Cheering", "Relaxing", "Trudging", "Cowering", "Pointing", "Lunging", "Dungeons", "Facepalm", "Sleeping" , "Dead", "Archer", "Kicking", "Reading", "High ground", "Clown", "Bitzel", "Pixel", "Profile"] 


@bot.slash_command(
    name="playercards",
    description="Generate a playercard!",
    guild_ids=[1471211723603050661],
)
async def playercards(
    ctx: discord.ApplicationContext,
    username: discord.Option(str, "Enter your username"),
    font: discord.Option(
        str,
        "Choose a font",
        choices=["Minecraft", "Minecraft Bold", "Trashhand (Life series font)"],
        default="Minecraft",
    ),
    colour: discord.Option(
        str,
        "Enter a hex colour code (e.g. FF5733)",
        default="FFFFFF",
    ),
    font_size: discord.Option(
        int,
        "Enter a font size (100-255)",
        min_value=100,
        max_value=255,
        default=100,
    ),
    pose: discord.Option(
        str,
        "Choose a pose",
        choices=POSE_CHOICES,
        default="Default",
    ),
    stat1: discord.Option(
        str,
        "Choose your first stat",
        choices=STAT_CHOICES,
        default="Final Kills",
    ),
    stat2: discord.Option(
        str,
        "Choose your second stat",
        choices=STAT_CHOICES,
        default="Kills",
    ),
    stat3: discord.Option(
        str,
        "Choose your third stat",
        choices=STAT_CHOICES,
        default="Average Kills per season",
    ),
    background: discord.Option(
        str,
        "Choose a background",
        choices=BACKGROUND_CHOICES,
        default="Enchanted Warped Forest",
    ),
):
    await ctx.defer()
    

    generate_player_card(
        user_input_username=username,
        user_input_font=font,
        user_input_colour=colour,
        user_input_font_size=font_size,
        pose=pose.lower(),
        statselection1=stat1,
        statselection2=stat2,
        statselection3=stat3,
        background_choice=background,
    )

    await ctx.respond(file=discord.File("stats.png"))


discord_token = os.getenv('DISCORD_TOKEN')






