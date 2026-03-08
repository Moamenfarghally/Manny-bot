import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import io
import asyncio
import json
import random

class ImageGen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Using Replicate with free model - no key needed for basic requests
        self.API_URL = "https://api.replicate.com/v1/predictions"
        self.MODEL = "stability-ai/sdxl"

    @app_commands.command(
        name="imagine",
        description="Generate an AI image from text"
    )
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer(thinking=True)

        try:
            # Using RunwayML's free test endpoint (no auth needed)
            async with aiohttp.ClientSession() as session:
                # Try Hugging Face's hosted inference for free (with rate limiting)
                headers = {
                    "User-Agent": "Mozilla/5.0"
                }
                
                # Using the Stable Diffusion XL turbo model via a free endpoint
                url = f"https://huggingface.co/spaces/stabilityai/stable-diffusion-xl"
                
                # Alternative: Direct image generation via free service
                safe_prompt = prompt.replace(" ", "+")
                direct_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=512&height=512&seed={random.randint(0, 1000000)}"
                
                async with session.get(
                    direct_url,
                    timeout=aiohttp.ClientTimeout(total=60),
                    ssl=False,
                    headers=headers
                ) as resp:
                    
                    if resp.status == 200:
                        image_bytes = await resp.read()
                        
                        image_file = discord.File(
                            io.BytesIO(image_bytes),
                            filename="generated.png"
                        )
                        
                        embed = discord.Embed(
                            title="🎨 Generated Image",
                            description=f"**Prompt:** {prompt}",
                            color=discord.Color.purple()
                        )
                        embed.set_image(url="attachment://generated.png")
                        
                        await interaction.followup.send(embed=embed, file=image_file)
                    elif resp.status == 403 or resp.status == 401:
                        await interaction.followup.send("⏳ Image generation is loading. Try again in a moment!")
                    else:
                        await interaction.followup.send(f"❌ Generation failed. Try again later!")

        except asyncio.TimeoutError:
            await interaction.followup.send("⏳ Taking too long. Try a shorter/simpler prompt!")
        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)[:100]}")


async def setup(bot):
    await bot.add_cog(ImageGen(bot))
