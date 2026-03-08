import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import aiohttp
import re

class Pinterest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pinterest",
        description="Search for images on Pinterest"
    )
    async def pinterest(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer(thinking=True)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
            
            # Use Pinterest search
            url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        return await interaction.followup.send(f"❌ Failed to search images")
                    
                    html = await resp.text()

            # Extract image URLs from Pinterest
            img_urls = re.findall(r'https://i\.pinimg\.com/[^\"\'\s<>]+', html)
            
            # Remove duplicates and limit to 9
            img_urls = list(dict.fromkeys(img_urls))[:9]

            if not img_urls:
                return await interaction.followup.send(f"❌ No images found for: `{query}`")

            embeds = []
            for i, url in enumerate(img_urls, 1):
                try:
                    embed = discord.Embed(
                        title=f"Image {i}",
                        color=discord.Color.from_rgb(230, 0, 35)
                    )
                    embed.set_image(url=url)
                    embeds.append(embed)
                except:
                    continue

            if embeds:
                await interaction.followup.send(
                    content=f"📌 **Pinterest search for:** `{query}` ({len(embeds)} images found)",
                    embeds=embeds
                )
            else:
                await interaction.followup.send(f"❌ Could not load images for: `{query}`")

        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ Request timed out. Try again later.")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}")


async def setup(bot):
    await bot.add_cog(Pinterest(bot))
