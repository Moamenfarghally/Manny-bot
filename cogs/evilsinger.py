import discord
from discord.ext import commands

GIF_URL = "https://cdn.discordapp.com/attachments/937444687155953745/1294971241400242237/evil_singer.gif"

class EvilSinger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="evilsinger",
        aliases=["es"]   # 👈 add more if you want
    )
    async def evilsinger_prefix(self, ctx):
        await ctx.send(GIF_URL)

async def setup(bot):
    await bot.add_cog(EvilSinger(bot))
