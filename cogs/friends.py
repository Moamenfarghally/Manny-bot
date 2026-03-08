import discord
from discord.ext import commands
from discord import app_commands

class Friends(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="friends", description="funny message")
    async def friends(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "haha u lonely ass aint getting friends go outside and find a bitch to friend ur lonely ass"
        )

async def setup(bot):
    await bot.add_cog(Friends(bot))
