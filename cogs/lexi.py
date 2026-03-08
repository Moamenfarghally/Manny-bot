import discord
from discord.ext import commands
import aiohttp
import random


class Lexi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_food_gif(self)
    
        food_searches = [
            "Burger", "Pizza", "Shrimp", "Sushi", "Pasta", "Ramen", "Fried Chicken", "Donuts", 
            "Cake", "Waffles", "Ice Cream", "Steak", "Curry", "Sandwich", "Spaghetti", "Fries",
            "Hot Dog", "Cheesecake", "Pancakes", "Bacon", "Lobster", "Crab", "Fish", "Salad",
            "Grilled Cheese", "Burrito", "Quesadilla", "Noodles", "Rice", "Chicken Wing", "Ribs",
            "Meatball", "Broccoli", "Apple Pie", "Brownie", "Cookie", "Croissant", "Espresso",
            "Hamburger", "French Toast", "Omelet", "Scrambled Eggs", "Avocado", "Beef", "Pork",
            "Turkey", "Salmon", "Shrimp Pasta", "Taco", "Enchilada", "Nachos", "Dip", "Chips"
        ]
        
        # Pick a random search term
        query = random.choice(food_searches)
        
        url = "https://g.tenor.com/v1/search"
        params = {
            "q": query,
            "key": "LIVDSRZULELA",  # public demo key
            "limit": 25
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()

        results = data.get("results", [])
        if not results:
            return None

        choice = random.choice(results)
        # Tenor v1 format
        return choice["media"][0]["gif"]["url"]

    @commands.command(name="lexi")
    async def lexi(self, ctx: commands.Context):
        gif_url = await self.get_food_gif()
        if not gif_url:
            return await ctx.send("❌ Couldn't fetch a food GIF right now.")
        await ctx.send(gif_url)


async def setup(bot):
    await bot.add_cog(Lexi(bot))
