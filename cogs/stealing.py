import discord
from discord.ext import commands
from discord import app_commands

# =============================
# 1) Define context-menu OUTSIDE the class
# =============================

@app_commands.context_menu(name="Steal Emoji_Sticker")
async def steal(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer()

    emoji_url = None

    # ---- Find custom emoji in text ----
    if message.content:
        for word in message.content.split():
            if word.startswith("<:") or word.startswith("<a:"):
                emoji_id = word.split(":")[-1].replace(">", "")
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
                break

    # ---- Find sticker ----
    if message.stickers:
        sticker = message.stickers[0]
        emoji_url = sticker.url

    if emoji_url is None:
        return await interaction.followup.send("❌ No emoji or sticker found in that message.")

    # ---- Build UI buttons ----
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Download Image", url=emoji_url))
    view.add_item(discord.ui.Button(label="Save as Emoji (Manual)", url=emoji_url))
    view.add_item(discord.ui.Button(label="Save as Sticker (Manual)", url=emoji_url))

    embed = discord.Embed(
        title="Steal Emoji / Sticker",
        description="Here is the file you requested:",
        color=discord.Color.green()
    )
    embed.set_image(url=emoji_url)

    await interaction.followup.send(embed=embed, view=view)

# =============================
# 2) Cog that registers the menu
# =============================

class StealEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(steal)   # register context menu

async def setup(bot):
    await bot.add_cog(StealEmoji(bot))
