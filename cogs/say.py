import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send")
    async def send_message(self, ctx, *, message: str):
        """Bot sends whatever message you type as fast as possible."""

        # Delete the message ASAP (fastest possible)
        try:
            await ctx.message.delete()
        except:
            pass

        # Bot sends the message
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Say(bot))