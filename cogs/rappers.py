import discord
from discord.ext import commands
import aiohttp
import random

class Rappers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tenor_api_key = "AIzaSyAyimkuYQYF_FXVALexPuGQctUWRURdCYQ"  # Public Tenor API key
        self.tenor_url = "https://tenor.googleapis.com/v2/search"  # Updated to v2 API
    
    async def get_rapper_gif(self, query: str):
        """Fetch a random GIF from Tenor based on the rapper query."""
        # Use random position to get different results each time
        random_pos = random.randint(0, 100)
        
        params = {
            "q": query,
            "key": self.tenor_api_key,
            "client_key": "discord_bot",
            "limit": 50,  # Increased limit for more variety
            "pos": str(random_pos)  # Random position for different results
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.tenor_url, params=params) as resp:
                    if resp.status != 200:
                        print(f"Tenor API returned status {resp.status}")
                        return None
                    
                    data = await resp.json()
                    results = data.get("results", [])
                    
                    if not results:
                        return None
                    
                    # Pick a random GIF from results
                    choice = random.choice(results)
                    # Tenor v2 format
                    return choice["media_formats"]["gif"]["url"]
        except Exception as e:
            print(f"Error fetching GIF from Tenor: {e}")
            return None
    
    # Playboi Carti
    @commands.command(name="carti", aliases=["CARTI", "Carti", "CaRtI", "cArTi"])
    async def carti(self, ctx: commands.Context):
        """Send a random Playboi Carti GIF"""
        gif_url = await self.get_rapper_gif("playboi carti rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't fetch a Carti GIF.")
        
        embed = discord.Embed(color=discord.Color.red())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # Ken Carson
    @commands.command(name="ken", aliases=["KEN", "Ken", "KeN", "kEn"])
    async def ken(self, ctx: commands.Context):
        """Send a random Ken Carson GIF"""
        gif_url = await self.get_rapper_gif("ken carson rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't fetch a Ken Carson GIF.")
        
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # NBA YoungBoy
    @commands.command(name="yb", aliases=["YB", "Yb", "yB", "youngboy", "YOUNGBOY", "YoungBoy"])
    async def yb(self, ctx: commands.Context):
        """Send a random NBA YoungBoy GIF"""
        gif_url = await self.get_rapper_gif("nba youngboy rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't fetch a YoungBoy GIF.")
        
        embed = discord.Embed(color=discord.Color.green())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # A$AP Rocky
    @commands.command(name="rocky", aliases=["ROCKY", "Rocky", "RoCkY", "rOcKy", "asap", "ASAP", "Asap"])
    async def rocky(self, ctx: commands.Context):
        """Send a random A$AP Rocky GIF"""
        gif_url = await self.get_rapper_gif("asap rocky rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't load an A$AP Rocky GIF.")
        
        embed = discord.Embed(color=discord.Color.purple())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # XXXTentacion
    @commands.command(name="x", aliases=["X", "xxxtentacion", "XXXTENTACION", "XXXTentacion", "Xxxtentacion"])
    async def xxxtentacion(self, ctx: commands.Context):
        """Send a random XXXTentacion GIF"""
        gif_url = await self.get_rapper_gif("xxxtentacion rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't find a gif.")
        
        embed = discord.Embed(color=discord.Color.dark_gray())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # Destroy Lonely
    @commands.command(name="lone", aliases=["LONE", "Lone", "LoNe", "lOnE", "lonely", "LONELY", "Lonely"])
    async def lone(self, ctx: commands.Context):
        """Send a random Destroy Lonely GIF"""
        gif_url = await self.get_rapper_gif("destroy lonely rapper")
        if not gif_url:
            return await ctx.send("❌ Couldn't find a gif.")
        
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
    
    # Tay (Custom)
    @commands.command(name="tay", aliases=["TAY", "Tay", "TaY", "tAy", "tayem", "TAYEM", "Tayem", "TayEm"])
    async def tayem(self, ctx: commands.Context):
        """Send a random fat person GIF"""
        gif_url = await self.get_rapper_gif("fat person")
        if not gif_url:
            return await ctx.send("❌ Couldn't find a gif.")
        
        embed = discord.Embed(color=discord.Color.orange())
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rappers(bot))