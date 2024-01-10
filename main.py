"""Discord Bot for luckerdogs"""
import os
import discord
from dotenv import load_dotenv
import responses


load_dotenv()

isProd = os.getenv("PROD", "")

CLIENT_ID = os.environ.get(
    "CLIENT_ID") if isProd else os.getenv("CLIENT_ID_DEV")
CLIENT_SECRET = os.environ.get(
    "CLIENT_SECRET") if isProd else os.getenv("CLIENT_SECRET_DEV")
TOKEN = os.environ.get("TOKEN") if isProd else os.getenv("TOKEN")


async def sendMessage(message, text):
    """Handler for sending messages to the corresponding Discord channel"""
    try:
        response = responses.handleResponses(message, text)
        await message.channel.send(response)
        await message.edit(suppress=True)
    except Exception as e:
        print(e)


def run():
    """Run for the Discord bot"""
    intents = discord.Intents.all()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        """Log connection on start"""
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        """Handle messages sent to the Discord channel"""
        if message.author == client.user:
            return

        userMessage = str(message.content)

        if userMessage[0] == '!':
            await sendMessage(message, userMessage)
    client.run(TOKEN)


if __name__ == "__main__":
    run()
