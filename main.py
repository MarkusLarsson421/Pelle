import asyncio
import datetime
import os
import discord
from discord import Intents, Colour
import pelle

TOKEN = os.environ.get("PELLE_TOKEN")
GUILD = "1212476737984794705"

intents = Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
is_running = True


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)

    # print(
    #     f"{client.user} is connected to the following guild:\n"
    #     f"{guild.name}(id: {guild.id})\n"
    # )
    #
    # members = "\n - ".join([member.name for member in guild.members])
    # print(f"Guild members:\n - {members}")
    #
    print("Starting API connection.")
    await update()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    match message.content:
        case "?status" | "?c":
            await message.channel.send(embed=status_embed())
        case "?json":
            await message.channel.send(pelle.get_json())
        case "?new_round":
            pelle.next_round()
        case "?update":
            pelle.update_api()


async def update():
    global is_running
    while is_running:
        pelle.update_api()
        if pelle.check_for_new_round():
            await new_round()
        await asyncio.sleep(300)


def status_embed():
    dictionary = pelle.get_status()

    color = Colour.pink()
    match dictionary["security_level"]:
        case "green":
            color = Colour.green()
        case "blue":
            color = Colour.blue()
        case "red":
            color = Colour.red()
        case "delta":
            color = Colour(000000)

    embed = discord.Embed(color=color)
    embed.add_field(name="Map", value=dictionary["map_name"], inline=True)
    embed.add_field(name="Security Level", value=dictionary["security_level"], inline=True)
    embed.add_field(name="Shuttle Status", value=dictionary["shuttle_mode"], inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Players", value=dictionary["players"], inline=True)
    embed.add_field(name="Admins", value=dictionary["admins"], inline=True)
    embed.add_field(name="Round Duration", value=datetime.timedelta(seconds=dictionary["round_duration"]), inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Round ID", value=dictionary["round_id"], inline=True)
    embed.add_field(name="Server Link", value="https://beestation13.com/join/bs_sage", inline=True)
    embed.set_footer(text="Named by speedy197.")
    return embed


async def new_round():
    channel = client.get_channel(1212476737984794708)
    await channel.send("<@184682379154161665>, there is a new round up coming!")


client.run(TOKEN)

