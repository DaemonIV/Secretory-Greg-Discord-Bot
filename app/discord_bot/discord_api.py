from dotenv import load_dotenv
import discord
import os
from app.chatgpt_ai.ai_client import chatgpt_response

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    #when ts starts up
    async def on_ready(self):
        print("Successfully logged in as: ", self.user)


    async def on_message(self, message):
        #this checks if the message isn't the bots
        if message.author == self.user:
            return
        print(message.content)

        command, user_message =None, None

        for text in ['/rules']:
            if message.content.startswith(text):
                command=message.content.split(' ')[0]
                user_message=message.content.replace(text, '')
                print(command, user_message)

        if command == '/rules':
            async with message.channel.typing():
                bot_response = chatgpt_response(prompt=user_message)
            await message.channel.send(f"{bot_response}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)





