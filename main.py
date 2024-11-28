import discord
from discord import app_commands, SelectOption
from discord.ext import commands
import os
import asyncio
from selenium_osu_client import OsuSeleniumClient
from osu_api_client_faceit import osuApiClient

DISCORD_BOT_TOKEN = os.getenv("osu!_discord_bot_token")
CLIEND_ID = os.getenv("osu_client_id")
CLIENT_SECRET = os.getenv("osu_client_secret")
osu_api_client = osuApiClient(client_id=CLIEND_ID, client_secret=CLIENT_SECRET)
osu_selenium_client = OsuSeleniumClient()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def display_osu_scores(beatmap_id, interaction: discord.Interaction):
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

        scores_embed.add_field(name=f"{score['username']}", value=f"➯ Score: {"{:,}".format(score['score'])}\n"
                                                                            f"➯ Accuracy: {score['accuracy']}%\n"
                                                                            f"➯ Rank: {score["rank"]}\n"
                                                                            f"➯ PP: {score['pp']}\n"
                                                                            f"➯ Mods: {score['mods']}\n"
                                                                            f"➯ Max Combo: {score['combo']}\n"
                                                                            f"➯ Date: {score['date']}", inline=False)
    await interaction.followup.send(embed=scores_embed)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def sync(ctx):
    print("sync command")
    if ctx.author.id == 301854099769655306:
        await bot.tree.sync()
        await ctx.send('Command tree synced.')
    else:
        await ctx.send('You must be the owner to use this command!')

class BeatmapsDropdown(discord.ui.Select):
    def __init__(self, beatmapset_data):
        self.beatmapset_data = beatmapset_data
        options = [discord.SelectOption(label=beatmap, description="", value=index) for index ,beatmap in enumerate(beatmapset_data["beatmap_names"])]
        super().__init__(placeholder="Choose a difficulty...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        selected_beatmap_index = self.values[0]
        selected_beatmap_id = self.beatmapset_data["beatmap_ids"][int(selected_beatmap_index)]
        await display_osu_scores(selected_beatmap_id, interaction=interaction)



class BeatmapsView(discord.ui.View):
    def __init__(self, beatmapset_data):
        super().__init__()
        self.dropdown = BeatmapsDropdown(beatmapset_data)
        self.add_item(self.dropdown)



@bot.tree.command(name='commands', description="All commands available")
async def help(interaction: discord.Interaction):
    commands_embed = discord.Embed(title="**Commands**", color=discord.Color.pink())
    commands_embed.set_footer(text="Developed By GaGex")
    commands_embed.add_field(name="check_faceit_beatmap_scores_id (beatmap id)", value=f"Here’s an example link to the beatmap: https://osu.ppy.sh/beatmapsets/983911#osu/2118443.\n The beatmap ID in this case is 2118443.\n (Graveyard maps dont work!)")
    commands_embed.add_field(name="check_faceit_scores (beatmap name)", value=f"Search for an osu! map with its name.\nchoose the desired difficulty, then shows faceit scores.")
    commands_embed.add_field(name="check_faceit_users_online", value="checks for all faceit osu! users who is online and who is not!")
    await interaction.response.send_message(embed=commands_embed)

@bot.tree.command(name='check_faceit_beatmap_scores_id', description="Checks all scores of faceit members with the given beatmap ID")
@app_commands.describe(beatmap_id="The beatmap ID in osu!")
async def check_scores(interaction: discord.Interaction, beatmap_id: int):
    await display_osu_scores(beatmap_id=beatmap_id, interaction=interaction)

@bot.tree.command(name="check_faceit_users_online", description="Checks for all osu! faceit users if they are online")
async def check_faceit_users_online(interaction: discord.Interaction):
    users_result = osu_api_client.get_faceit_users_info()
    if len(users_result) > 0:
        users_online_embed = discord.Embed(title="All faceit users who are online!", description="(Also shows the online users on the site not only in game!)")
        for username, user_info in users_result.items():
            user_global_rank = "{:,}".format(user_info["global_rank"])
            is_user_online = user_info["is_online"]
            if is_user_online:
                is_user_online = ":green_circle:"
            else:
                is_user_online = ":red_circle:"
            users_online_embed.add_field(name=username, value=f"Global Rank: {user_global_rank}#\nOnline: {is_user_online}", inline=False)
    else:
        await interaction.response.send_message("Couldn't fetch data, ask gal why?")
        return
    await interaction.response.send_message(embed=users_online_embed)



@bot.tree.command(name="check_faceit_scores", description="Upgraded and more comfortable way of checking faceit scores")
@app_commands.describe(beatmapset_name="Beatmapset Name...")
async def check_scores_by_name(interaction: discord.Interaction, beatmapset_name: str):
    await interaction.response.defer()
    try:
        data = osu_selenium_client.osu_beatmapset_search(beatmapset_name=beatmapset_name)
    except Exception as e:
        await interaction.followup.send("**Could not find the map you were looking for, be more specific (artist/band/mapped by..)**")
        print("Exception happened when tried to get difficulties names.", e)
        return
    else:
        beatmap_embed = discord.Embed(title=f"Found The Map: **{data["beatmap_title"]}**", description="Choose the difficulty of the map...")
        beatmap_embed.set_image(url=data["beatmap_image_url"])
        beatmap_embed.set_footer(text="Developed By GaGex")
        beatmap_embed.color = discord.colour.Color.pink()
        initial_message = await interaction.followup.send(view=BeatmapsView(data), embed=beatmap_embed, ephemeral=True)
        await asyncio.sleep(60)
        await initial_message.delete()

bot.run(token=DISCORD_BOT_TOKEN)