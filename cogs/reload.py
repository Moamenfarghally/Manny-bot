import discord
from discord.ext import commands
from discord import app_commands
import os

class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Only allow the bot owner to run this
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in [856537385810657290, 1207820837692899400]:
            await interaction.response.send_message("❌ You cannot use this command.", ephemeral=True)
            return False
        return True

    @app_commands.command(name="reload", description="Reload a cog or all cogs instantly.")
    @app_commands.describe(cog="Name of a cog (leave empty to reload all)")
    async def reload(self, interaction: discord.Interaction, cog: str | None = None):

        await interaction.response.defer(ephemeral=True)

        if cog is None:
            # Reload all cogs
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    try:
                        await self.bot.reload_extension(f"cogs.{name}")
                    except Exception as e:
                        return await interaction.followup.send(f"❌ Error reloading `{name}`:\n```\n{e}\n```")

            await self.bot.tree.sync()
            return await interaction.followup.send("🔄 **Reloaded ALL cogs successfully!**")

        # Reload one cog
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            return await interaction.followup.send(f"🔄 Reloaded `{cog}` successfully!")

        except Exception as e:
            return await interaction.followup.send(f"❌ Failed to reload `{cog}`:\n```\n{e}\n```")


async def setup(bot):
    await bot.add_cog(ReloadCog(bot))
