import discord
from discord import app_commands
from discord.ext import commands
from urllib.parse import quote_plus

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="search", description="Search something on Google.")
    async def search(self, interaction: discord.Interaction, query: str):

        # Prevent Discord timeout
        await interaction.response.defer()

        # Create Google search link
        url = f"https://www.google.com/search?q={quote_plus(query)}"

        # Send result
        await interaction.followup.send(f"<:flushed_peach:1439264302237225103>**Google Search Result:**\n{url}")

async def setup(bot):
    await bot.add_cog(Search(bot))
