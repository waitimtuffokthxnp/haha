import discord
from discord.ext import commands
from discord import app_commands
import os
import random
import requests
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())

# -----------------------------
# GLOBAL AIOHTTP SESSION (IMPORTANT)
# -----------------------------
session: aiohttp.ClientSession | None = None


FILES = [
    "03137d3096875861.txt", "129521809f206cc2.txt", "21c8125db11e7793.txt",
    "25ec9ff80ff99697.txt", "2898c681c6151598.txt", "29de2c9bb0d1aa39.txt",
    "2c1421e20f401388.txt", "4356d8426dd214b2.txt", "5c5d695a0d4c0436.txt",
    "63b2443f78cc5744.txt", "683cb837769fbf9d.txt", "69d3de3f3ce1f1fc.txt",
    "6d53bc6fd4248fc1.txt", "6d53ef61eb1e673f.txt", "83dff351c98d4a69.txt",
    "85c614a316b076d1.txt", "8aaa09faab1dac12.txt", "9864766a09ac7b3f.txt",
    "a0fa0680478e86ae.txt", "a4b32c9a3f0f489d.txt", "a6aae849b155b4d6.txt",
    "afce701f8b690bec.txt", "b654ad00ccb3ff08.txt", "bac8ff328543f18b.txt",
    "bdb627dd786814e5.txt", "c41277f57a66a917.txt", "c8a710654700e75c.txt",
    "cf003e75da5d2d90.txt", "d2a081b32720146c.txt", "ec3f20794c42d556.txt",
    "f0b2d8a7d9c6a2ab.txt",
]


async def uwuify_text(text: str, provider: str = "uwuify"):
    global session

    payload = { "text": text, "provider": provider }

    try:
        async with session.post("https://uwu.pm/api/v1/uwu", json=payload, timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status != 200:
                return None, f"HTTP {response.status}"

            data = await response.json()
            result = data.get("text") or data.get("uwu") or str(data)

            return result, None

    except Exception as e:
        return None, str(e)

@client.event
async def on_ready():
    global session

    session = aiohttp.ClientSession()

    await client.tree.sync()
    print("Bot ready!")


# slash cmds

@client.tree.command(name="version", description="fetch current RBXL version")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def version(interaction: discord.Interaction):
    try:
        data = requests.get("https://weao.xyz/api/versions/current", timeout=10).json()

        embed = discord.Embed(color=0xC75456)
        embed.add_field(name="Version", value=data.get("Windows", "idk"), inline=False)
        embed.add_field(name="Date", value=data.get("WindowsDate", "idk"), inline=False)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message(f"error: {e}", ephemeral=True)

@client.tree.command(name="iqsm", description="sends a iqsm")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def iqsm(interaction: discord.Interaction):
    file = random.choice(FILES)
    url = f"https://raw.githubusercontent.com/xwxfox/boykisser/main/ascii/sfw/{file}"
    response = requests.get(url)

    if response.status_code == 200:
        ascii_art = response.text

        if len(ascii_art) > 1989:
            ascii_art = ascii_art[:1989] + "\n..."

        await interaction.response.send_message(ascii_art)
    else:
        await interaction.response.send_message("failed to fetch a file", ephemeral=True)

@client.tree.command(name="uwuify", description=">_<")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(text="text", provider="provider")
@app_commands.choices(provider=[ app_commands.Choice(name="uwuify", value="uwuify"), app_commands.Choice(name="uwwwupp", value="uwwwupp") ])
async def uwuify_command(interaction: discord.Interaction,  text: str, provider: app_commands.Choice[str] | None = None):
    selected_provider = provider.value if provider else "uwuify"
    result, error = await uwuify_text(text, selected_provider)
    
    if error:
        return await interaction.response.send_message(f"({error})")

    await interaction.response.send_message(result)


# content menu lol

@client.tree.context_menu(name="uwuify")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def uwuify_message(interaction: discord.Interaction, message: discord.Message):
    result, error = await uwuify_text(message.content, "uwuify")

    if error:
        return await interaction.response.send_message(f"({error})")

    await interaction.response.send_message(result)

@client.tree.context_menu(name="uwwwupp")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def uwuify_uwwwupp(interaction: discord.Interaction, message: discord.Message):
    result, error = await uwuify_text(message.content, "uwwwupp")

    if error:
        return await interaction.response.send_message(f"({error})")

    await interaction.response.send_message(result)

async def close_session():
    global session
    if session:
        await session.close()


client.run(os.getenv("token"))
