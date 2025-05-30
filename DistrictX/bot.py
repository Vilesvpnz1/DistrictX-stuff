import os
import json
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import requests
from base64 import b64encode, b64decode

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
SCHOOLS_PATH = os.getenv("SCHOOLS_PATH", "schools.json")
CONTRIBUTORS_PATH = os.getenv("CONTRIBUTORS_PATH", "contributors.json")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def github_api_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_file_content(path):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}?ref={GITHUB_BRANCH}"
    r = requests.get(url, headers=github_api_headers())
    r.raise_for_status()
    content = r.json()
    return b64decode(content['content']).decode(), content['sha']

def update_file(path, new_content, message):
    _, sha = get_file_content(path)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    data = {
        "message": message,
        "content": b64encode(new_content.encode()).decode(),
        "branch": GITHUB_BRANCH,
        "sha": sha
    }
    r = requests.put(url, headers=github_api_headers(), json=data)
    r.raise_for_status()
    return r.json()

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

@bot.tree.command(name="listschools", description="List all schools")
async def list_schools(interaction: discord.Interaction):
    content, _ = get_file_content(SCHOOLS_PATH)
    schools = json.loads(content)
    await interaction.response.send_message(f"Schools: {', '.join([s['name'] for s in schools])}")

# TODO: Add /addschool, /editschool, /deleteschool, /addcontributor, /removecontributor, /listcontributors

bot.run(DISCORD_TOKEN) 