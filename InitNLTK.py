import nltk
import random
nltk.download('wordnet')
nltk.download('names')

import discord
import asyncio

TOKEN = "MTM2NjgyNTk0MzYzNjkwMTg5OA.GTcMpr.fra_P6qHVey8G0ap8SXbjumrgQHyU35_ioJRC0"  # Replace with your actual token
CHANNEL_ID = 1366496525890355260  # Replace with your channel ID (currently set to the idek channel)
MESSAGE = "i like bombs."  # Replace with the word or message you want to spam
# 1366496525890355260 - idek
# 1364982782350327821 - general
intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Could not find the channel. Check CHANNEL_ID and bot permissions.")
        return

    # Infinite spam loop
    while True:
        await channel.send(MESSAGE)
        await asyncio.sleep(0.1)  #Change the number if you want to change frequency

client.run(TOKEN)
