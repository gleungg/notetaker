import discord
import os
import db, responses
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TOKEN = os.environ.get("TOKEN")

async def sendMessage(message, text):
    try: 
        response = responses.handle_responses(message, text)
        await message.channel.send(response)
        await message.edit(suppress=True)
    except Exception as e:
        print(e)

def run():
    intents = discord.Intents.all()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        userMessage = str(message.content)

        if userMessage[0] == '!':
            await sendMessage(message, userMessage)
    client.run(TOKEN)

if __name__ == "__main__":
    run()