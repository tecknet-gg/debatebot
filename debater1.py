import discord
import asyncio
import json

# Load debate data from the JSON file
with open("debateData.json") as json_file:
    debateData = json.load(json_file)

# Tokens and IDs for the bots
bot1token = "MTM2NjgyNTk0MzYzNjkwMTg5OA.GMXn3S.ZiLp6kuSsqNxgeuiQO4It2eseOz6PpqteCL5hE"
bot1name = debateData["persona1name"]
bot2name = debateData["persona2name"]
channelID = 1367513947413942272
bot2ID = 1367478976578060288

contextFile = "context.json"

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)


async def last5(channelID):
    messages = []
    with open("messagesSent.json", "r") as file:
        messagesSent = json.load(file)["messagesSent"]

    # Get the channel and iterate through message history
    channel = client.get_channel(channelID)
    async for msg in channel.history(limit=100):
        if len(messages) == 5 or messagesSent == 0:
            break

        if len(messages) == messagesSent:
            break

        if msg.author.id in {client.user.id, bot2ID}:
            messages.append({"author": str(msg.author), "content": msg.content})

    # Replacing author names after gathering the messages
    for message in messages:
        if message["author"] == "Chuck#2793":
            message["author"] = bot2name
        else:
            message["author"] = bot1name

    return list(reversed(messages))

async def updateLoop():
    await client.wait_until_ready()
    channel = client.get_channel(channelID)

    while not client.is_closed():
        try:
            with open('arguements.json', 'r') as args_file:
                args = json.load(args_file)
            # Only send if there's a message
            if args[0]["bot1"].strip():
                await channel.send(args[0]["bot1"])
                initial_data = [
                    {
                        "bot1": "",
                        "bot2": ""
                    }
                ]
                await asyncio.sleep(1)
                with open("arguements.json", "w") as file:
                    json.dump(initial_data, file, indent=4)

                # Update context
                recent = await last5(channelID)
                with open('context.json', 'w') as context_file:
                    json.dump(recent, context_file, indent=4)

        except Exception as e:
            print(f"Error in updateLoop: {e}")

        await asyncio.sleep(1)


@client.event
async def on_ready():
    initial_data = [
        {
            "bot1": "",
            "bot2": ""
        }
    ]
    with open("arguements.json", "w") as file:
        json.dump(initial_data, file, indent=4)
    print(f"Logged in as {client.user}")

    guild = client.get_guild(1364982781796552827)
    if guild:
        botMember = guild.get_member(client.user.id)
        if botMember:
            await botMember.edit(nick=f"{bot1name}")
            print("Bot's nickname changed successfully!")
        else:
            print("Bot is not a member of the guild.")
    else:
        print("Guild not found.")
    client.loop.create_task(updateLoop())


def startBot1():
    client.run(bot1token)

startBot1()