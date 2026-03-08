import discord
from discord.ext import commands
from discord import app_commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Check if the bot is online")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hey there! 👋 I'm alive!")

async def setup(bot):
    await bot.add_cog(Hello(bot))
