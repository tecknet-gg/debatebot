import discord
import asyncio
import json

with open('debateData.json') as json_file:
    debateData = json.load(json_file)

bot2token = "MTM2NzQ3ODk3NjU3ODA2MDI4OA.GJz-JH.yOobgHnTWowqLYYzFghSR_eCZIEtWcrhTqBgoI"
bot1name = debateData["persona1name"]
bot2name = debateData["persona2name"]
channelID = 1367513947413942272  # Ensure "channelID" exists in your debateData.json
bot2ID = 1367478976578060288

client = discord.Client(intents=discord.Intents.default())
async def last5(channelID):
    messages = []
    with open("messagesSent.json", "r") as file:
        messagesSent = json.load(file)["messagesSent"]
    channel = client.get_channel(channelID)
    async for msg in channel.history(limit=100):
        if len(messages) == 5 or messagesSent == 0:
            break

        if len(messages) == messagesSent:
            break

        if msg.author.id in {client.user.id, bot2ID}:
            messages.append({"author": str(msg.author), "content": msg.content})

    for message in messages:
        if message["author"] == "Chuck#2793":
            message["author"] = bot2name
        else:
            message["author"] = bot1name

    return list(reversed(messages))

async def updateLoop():
    await client.wait_until_ready()
    channel = client.get_channel(channelID)
    prevMessage = ""
    while not client.is_closed():
        try:
            with open('arguements.json', 'r') as args_file:
                args = json.load(args_file)
                if args[0]["bot2"].strip():
                    if prevMessage == args[0]["bot2"]:
                        pass
                    else:
                        await channel.send(args[0]["bot2"])
                    prevMessage = args[0]["bot2"]
                    args[0]["bot2"] = ""
                    with open("arguements.json", "w") as file:
                        json.dump(args, file, indent=4)

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
            await botMember.edit(nick=f"{bot2name}")
            print("Bot's nickname changed successfully!")
        else:
            print("Bot is not a member of the guild.")
    else:
        print("Guild not found.")
    client.loop.create_task(updateLoop())


def startBot2():
    client.run(bot2token)  # Run the bot with the token

startBot2()