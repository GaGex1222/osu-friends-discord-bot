import discord
from discord import app_commands, SelectOption
from discord.ext import commands
import os
import asyncio
from osu_api_client_faceit import osuApiClient

DISCORD_BOT_TOKEN = os.getenv("osu!_discord_bot_token")
CLIEND_ID = os.getenv("osu_client_id")
CLIENT_SECRET = os.getenv("osu_client_secret")
osu_api_client = osuApiClient(client_id=CLIEND_ID, client_secret=CLIENT_SECRET)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

# @bot.tree.command(name='commands', description="All commands available")
# async def help(interaction: discord.Interaction):
#     awa

@bot.tree.command(name='check_faceit_beatmap_score', description="Checks all scores of faceit members with the given beatmap ID")
@app_commands.describe(beatmap_id="The beatmap ID in osu!")
async def check_scores(interaction: discord.Interaction, beatmap_id: int):
    await interaction.response.defer()
    scores = osu_api_client.get_faceit_beatmap_scores(beatmap_id=beatmap_id)
    beatmap_info = osu_api_client.get_beatmap_info(beatmap_id=beatmap_id)

    if not beatmap_info:
        await interaction.followup.send("Could not retrieve beatmap information.")
        return

    scores_embed = discord.Embed(
        title=f"Faceit scores for {beatmap_info['title']} [{beatmap_info['version']}]",
        description="If you are not listed here you dont have a score on this map!",
        color=discord.Color.pink()
    )
    
    scores_embed.set_image(url=beatmap_info["image"])
    scores_embed.set_footer(text="Developed by GaGex", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Osu%21_Logo_2016.svg/768px-Osu%21_Logo_2016.svg.png")
    for score in scores:
        player_info = osu_api_client.get_user_info(user_id=score["user_id"])
        player_image = player_info["avatar"]

        scores_embed.add_field(name=f"Username: {score['username']}", value=f"Max Combo: {score['combo']}\n"
                                                                            f"Accuracy: {score['accuracy']}%\n"
                                                                            f"Mods: {score['mods']}\n"
                                                                            f"PP: {score['pp']}\n"
                                                                            f"Score: {score['score']}\n"
                                                                            f"Rank: {score["rank"]}\n"
                                                                            f"Date: {score['date']}", inline=False)
    await interaction.followup.send(embed=scores_embed)
bot.run(token=DISCORD_BOT_TOKEN)