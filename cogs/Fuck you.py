import discord
from discord import app_commands

@app_commands.context_menu(name="Fuck You")
async def fuck_you(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(
        "Manny says fuck you",
        allowed_mentions=discord.AllowedMentions.none()
    )

async def setup(bot):
    bot.tree.add_command(fuck_you)
