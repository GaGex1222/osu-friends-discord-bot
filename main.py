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

@bot.tree.command(name='commands', description="All commands available")
async def help(interaction: discord.Interaction):
    commands_embed = discord.Embed(title="Commands", color=discord.Color.pink())
    commands_embed.set_footer(text="Developed By GaGex")
    commands_embed.add_field(name="check_faceit_beatmap_scores (beatmap id)", value=f"Here’s an example link to the beatmap: https://osu.ppy.sh/beatmapsets/983911#osu/2118443.\n The beatmap ID in this case is 2118443.\n (Graveyard maps dont work!)")
    await interaction.response.send_message(embed=commands_embed)

@bot.tree.command(name='check_faceit_beatmap_scores', description="Checks all scores of faceit members with the given beatmap ID")
@app_commands.describe(beatmap_id="The beatmap ID in osu!")
async def check_scores(interaction: discord.Interaction, beatmap_id: int):
    await interaction.response.defer()
    try:
        scores = osu_api_client.get_faceit_beatmap_scores(beatmap_id=beatmap_id)
        beatmap_info = osu_api_client.get_beatmap_info(beatmap_id=beatmap_id)
    except Exception as e:
        await interaction.followup.send("Could not retrieve information - check the beatmap id provided.")
        return

    scores_embed = discord.Embed(
        title=f"Faceit scores for {beatmap_info['title']} [{beatmap_info['version']}]",
        description="If you are not listed here you dont have a score on this map!",
        color=discord.Color.pink()
    )
    
    scores_embed.set_image(url=beatmap_info["image"])
    scores_embed.set_footer(text="Developed By GaGex")
    for score in scores:
        player_info = osu_api_client.get_user_info(user_id=score["user_id"])
        player_image = player_info["avatar"]

        scores_embed.add_field(name=f"Username: {score['username']}", value=f"Profile picture: {player_image}\n"
                                                                            f"Max Combo: {score['combo']}\n"
                                                                            f"Accuracy: {score['accuracy']}%\n"
                                                                            f"Mods: {score['mods']}\n"
                                                                            f"PP: {score['pp']}\n"
                                                                            f"Score: {"{:,}".format(score['score'])}\n"
                                                                            f"Rank: {score["rank"]}\n"
                                                                            f"Date: {score['date']}", inline=False)
    await interaction.followup.send(embed=scores_embed)
bot.run(token=DISCORD_BOT_TOKEN)