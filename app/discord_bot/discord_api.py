from dotenv import load_dotenv
import discord
import os
from app.chatgpt_ai.ai_client import chatgpt_response

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True



bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('------------------------------')
    print("B")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)
    


@bot.slash_command(name="rules", description="Get the rules of the server", guild_ids=[1471211723603050661])
async def rules(ctx: discord.ApplicationContext, prompt: discord.Option(str, "Enter your questions about the rules of the server")):
    print(prompt)
    await ctx.defer()
    bot_response = chatgpt_response(prompt=prompt)
    await ctx.respond(f"{bot_response}")

@bot.slash_command(name="Playercards", description="Generate a playercard!", guild_ids=[1471211723603050661])
async def playercards(
    ctx: discord.ApplicationContext, 
    username: discord.Option(str, "Enter your username"),
    font: discord.Option(str, "Choose a font", choices=["Minecraft", "Minecraft Bold", "Trashhand (Life series font)"]), required=True, default="Minecraft",
    colour: discord.Option(str, "Enter a hex colour code (e.g. FF5733)"), required=True, default="FFFFFF",
    font_size: discord.Option(int, "Enter a font size (100-255)"), required=True, default=99,
    ):

discord_token = os.getenv('DISCORD_TOKEN')






